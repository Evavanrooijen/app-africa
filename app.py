from functions import *
import streamlit as st

st.title('Forecasting African GDP Growth')
T = st.sidebar.slider('Select Time Horizon (T): ', 10, 100,50)
N = st.sidebar.slider('Select #Countries (N): ', 10, 100,50)
var_eps = st.sidebar.selectbox('Select variance of epsilon',[0.5, 1])
alpha = st.sidebar.selectbox('Select alpha',[2, 5, 10])

st.write('Generate Data by specifying parameters in the sidebar.')

@st.cache
def simulate_date(N, T, alpha, var_eps):
  """ Function that takes all parameters and returns a simulated dataset [NxT]"""
  return create_DGP(N, T, alpha, var_eps)

@st.cache
def run_example_param(Y, i, a, tao):
    JH, pos, neg, self_gr, params, rank = define_parameters(Y, i, tao)
    # beaten, predictions, predictions_IMA, truth, fittedParams, params, rank, JH, pos, neg
    return run_single_simulation(Y, i,a, tao)

Y = simulate_date(N, T, alpha, var_eps)

if st.sidebar.button('Generate Data'):
    Y = simulate_date(N, T, alpha, var_eps)


if st.checkbox('Show Example', value=False):
    i = st.slider('Select Country (i): ', 0, N,0)
    st.write('GDP Levels Country {}'.format(i))
    st.line_chart(Y[i])
    st.write('GDP Growth Country {}'.format(i))
    st.line_chart(growth_rate(Y[i]))


    if st.checkbox('Estimate Model for Single Country', value=False):
        a = st.selectbox('Select a',[1, 2, 5,  10])
        tao = st.selectbox('Select tao',[0.4, 0.7], index=1)

        beaten, predictions, predictions_IMA, truth, fittedParams, params, rank, JH, pos, neg = run_example_param(Y, i,a, tao)

        st.write('Step 1: CRDW')

        st.write('We find {} cointegration series'.format(rank-1))
        if st.checkbox('Show Time Series'):
            st.dataframe(JH)
            st.line_chart(np.transpose(JH[:, 1:]))

        st.write('Step 2: Correlations')
        format = st.selectbox('Select a visualization', ['Table', 'Plot'])
        if st.checkbox('Show Highest Correlation Series'):
            # show country with correlation value instead of messy plot
            if format == 'Table':
                st.dataframe(pos)
            if format == 'Plot':
                st.line_chart(np.transpose(pos))
        if st.checkbox('Show Lowest Correlation Series'):
            if format == 'Table':
                st.dataframe(neg)
            if format == 'Plot':
                st.line_chart(np.transpose(neg))

        st.write('Step 3: Define Parameters')
        # st.write('optional to add initialization values here')
        if st.checkbox('Show Initial Parameter Values'):
            for name, value in params.valuesdict().items():
                st.write(name, value)

        st.write('Step 4: Model Fitting')

        st.write('Predictions')
        st.line_chart(predictions)
        #predictions, predictions_IMA, truth, RMSPE_i, RMSPE_IMA_i, params = run_single_estimation2(Y, i, t, 2)
        if st.checkbox('Show Fitted Parameter Values'):
            for name, value in fittedParams.valuesdict().items():
                st.write(name, value)
                
        RMSPE_i = calculate_RMSPE(predictions, truth)
        RMSPE_IMA_i = calculate_RMSPE(predictions_IMA, truth)
        st.write('RMSPE for country {} is {} for our model against a benchmark of {}'.format(i, RMSPE_i, RMSPE_IMA_i))

        st.write('## Residuals')
        st.line_chart(predictions-truth)
        # fit and plot IMA(1, 1)
        st.write('## IMA Model Residuals')
        st.line_chart(predictions_IMA-truth)
        # table with RMSPE comparison
        st.write('## Model Comparison')
        st.line_chart(np.transpose([predictions, predictions_IMA, truth]))
"""
    runs = st.selectbox('Select #runs (runs): ', [1, 10, 50, 100, 150, 200], index=0)
    st.write('## Simulation runs')
    scoresBeaten = np.zeros(runs)
    for run in range(runs):
        Y = create_DGP(N, T, alpha, var_eps)
        scoresBeaten[run] = run_simulation(Y,a, tao)
    beatenScore = np.mean(scoresBeaten)
    beatenStd = np.std(scoresBeaten)
    st.write('Over {} runs, we beat the benchmark on average for {} out of {} countries'.format(runs, beatenScore, N))
    st.write('H0: beaten == N/2')
    st.write(scoresBeaten)
    ttest = (beatenScore-N/2)/(beatenStd/sqrt(runs))
    st.write('t-test ouput: {}'.format(ttest))
"""
    #st.write('## Model Comparison')
    #st.write('For {} countries and a time horizon of {}, we beat the benchmark {} out of {} times.'.format(N, T, np.sum(scoresBeaten), runs*N))
