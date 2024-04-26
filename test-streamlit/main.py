import logging
import os
import time

import streamlit as st
import numpy as np

import sentry_sdk


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    enable_tracing=True,
    debug=True,
)

# Configure logging (adjust level as needed)
logging.basicConfig(level=logging.DEBUG)
st_logger = logging.getLogger('streamlit')
st_logger.setLevel(logging.INFO)


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

with sentry_sdk.start_transaction(op="function", name="streamlit_test"):
    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

        bla = 1 / (i-50)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")