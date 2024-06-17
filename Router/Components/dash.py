
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
import pandas as pd

def Analysis_dash(statu_active,st):
    if st.toggle("Display Visualization", value=statu_active, disabled=False):
        if not st.session_state.multi_task_df:
            st.error("No data available. Please ensure there a Prediction Tasks in Session  to comp")
        else:
            st.subheader(f"Visualization Statu {statu_active}")
            multi_task_df = st.session_state.multi_task_df[-1]

            # Create Plotly subplots for predicted durations, minimum hours, and maximum hours
            fig1 = make_subplots(rows=1, cols=2, subplot_titles=("Predicted Duration (Hours)", "Duration Distribution"))

            # Add bar plot for predicted durations with different colors
            fig1.add_trace(go.Bar(
                x=multi_task_df['Task'],
                y=multi_task_df['Predicted_Duration_Hours'],
                marker=dict(color=multi_task_df['Predicted_Duration_Hours'], colorscale='Viridis'),
                name='Predicted Duration (Hours)'
            ), row=1, col=1)

            # Add box plot for the duration distribution
            fig1.add_trace(go.Box(
                y=multi_task_df['Predicted_Duration_Hours'],
                marker=dict(color='rgb(55, 83, 109)'),
                name='Predicted Duration (Hours)',
                boxpoints='all',  # Show all points
                jitter=0.5  # Add some jitter to the points
            ), row=1, col=2)

            # Update layout
            fig1.update_layout(
                title='Task Duration Analysis',
                xaxis_title='Task',
                yaxis_title='Duration (Hours)',
                xaxis_tickangle=-45,
                width=1200,
                height=600
            )

            # Show plot
            st.plotly_chart(fig1)

            # Create a second set of subplots for the pie chart and Gantt chart
            fig2 = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "xy"}]], subplot_titles=("Predicted Duration Distribution", "Task Timeline"))

            # Add pie chart for predicted durations with different colors
            fig2.add_trace(go.Pie(
                labels=multi_task_df['Task'],
                values=multi_task_df['Predicted_Duration_Hours'],
                marker=dict(colors=multi_task_df['Predicted_Duration_Hours']),
                name='Predicted Duration Distribution'
            ), row=1, col=1)

            # Convert datetime columns to datetime objects
            multi_task_df['Current_Time'] = pd.to_datetime(multi_task_df['Current_Time'])
            multi_task_df['Estimated_Finished_Date'] = pd.to_datetime(multi_task_df['Estimated_Finished_Date'])

            # Add Gantt-like chart for task progress with different colors
            for i, row in multi_task_df.iterrows():
                fig2.add_trace(go.Scatter(
                    x=[row['Current_Time'], row['Estimated_Finished_Date']],
                    y=[row['Task'], row['Task']],
                    mode='lines+markers',
                    name=row['Task'],
                    line=dict(color='rgb(0, 176, 246)', width=2),
                    marker=dict(size=10, color='rgb(0, 176, 246)')
                ), row=1, col=2)

            # Update layout
            fig2.update_layout(
                title='Task Duration Analysis',
                xaxis_title='Date',
                yaxis_title='Task',
                xaxis_tickangle=-45,
                width=1200,
                height=600
            )

            # Show plot
            st.plotly_chart(fig2)