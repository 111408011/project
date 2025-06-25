import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Page configuration
st.set_page_config(
    page_title="Enterprise Payment Processing Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    /* Custom header */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .dashboard-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .dashboard-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Professional metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.04);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    
    /* System cards */
    .system-card {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .system-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .system-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #10b981, #059669);
    }
    
    .system-card.warning::before {
        background: linear-gradient(90deg, #f59e0b, #d97706);
    }
    
    .system-card.error::before {
        background: linear-gradient(90deg, #ef4444, #dc2626);
    }
    
    .system-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .system-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }
    
    .system-id {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 500;
        background: #f3f4f6;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin-top: 0.3rem;
    }
    
    .status-badge {
        font-size: 1.8rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-item {
        text-align: center;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    
    /* Professional buttons */
    .analytics-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .analytics-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Status indicators */
    .status-healthy { color: #10b981; }
    .status-warning { color: #f59e0b; }
    .status-error { color: #ef4444; }
    
    /* Section headers */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 1px;
        margin: 1.5rem 0;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        font-family: 'Inter', sans-serif;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .dashboard-title {
            font-size: 2rem;
        }
        .metrics-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_system' not in st.session_state:
    st.session_state.selected_system = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

def create_enterprise_sample_data():
    """Create realistic enterprise-grade sample data"""
    
    # Simulate real-world payment volumes with patterns
    current_hour = datetime.now().hour
    base_multiplier = 1.2 if 9 <= current_hour <= 17 else 0.7  # Business hours effect
    
    return {
        'channels': [
            {
                'id': 'CH-FG-001',
                'name': 'Enterprise File Gateway',
                'type': 'SWIFT/ISO20022',
                'total': int(2847 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(2847 * base_multiplier * 0.94 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(2847 * base_multiplier * 0.04 * np.random.uniform(0.5, 1.5)),
                'rejected': int(2847 * base_multiplier * 0.02 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'EU-WEST',
                'uptime': 99.7
            },
            {
                'id': 'CH-API-002',
                'name': 'Real-time API Gateway',
                'type': 'REST/GraphQL',
                'total': int(1923 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(1923 * base_multiplier * 0.97 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(1923 * base_multiplier * 0.02 * np.random.uniform(0.5, 1.5)),
                'rejected': int(1923 * base_multiplier * 0.01 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'US-EAST',
                'uptime': 99.9
            },
            {
                'id': 'CH-MOB-003',
                'name': 'Mobile Banking Channel',
                'type': 'Native/Hybrid',
                'total': int(1156 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(1156 * base_multiplier * 0.96 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(1156 * base_multiplier * 0.03 * np.random.uniform(0.5, 1.5)),
                'rejected': int(1156 * base_multiplier * 0.01 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'APAC',
                'uptime': 99.8
            },
            {
                'id': 'CH-WEB-004',
                'name': 'Web Portal Channel',
                'type': 'SPA/PWA',
                'total': int(892 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(892 * base_multiplier * 0.93 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(892 * base_multiplier * 0.05 * np.random.uniform(0.5, 1.5)),
                'rejected': int(892 * base_multiplier * 0.02 * np.random.uniform(0.8, 1.2)),
                'status': 'warning',
                'region': 'EU-CENTRAL',
                'uptime': 98.9
            }
        ],
        'preprocessors': [
            {
                'id': 'PP-VAL-001',
                'name': 'Advanced Validation Engine',
                'type': 'ML/Rules-Based',
                'total': int(4567 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(4567 * base_multiplier * 0.96 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(4567 * base_multiplier * 0.03 * np.random.uniform(0.5, 1.5)),
                'rejected': int(4567 * base_multiplier * 0.01 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'GLOBAL',
                'uptime': 99.95
            },
            {
                'id': 'PP-AML-002',
                'name': 'AML/Sanctions Screening',
                'type': 'AI/Compliance',
                'total': int(4234 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(4234 * base_multiplier * 0.92 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(4234 * base_multiplier * 0.06 * np.random.uniform(0.5, 1.5)),
                'rejected': int(4234 * base_multiplier * 0.02 * np.random.uniform(0.8, 1.2)),
                'status': 'warning',
                'region': 'GLOBAL',
                'uptime': 99.1
            },
            {
                'id': 'PP-FRD-003',
                'name': 'Fraud Detection Engine',
                'type': 'ML/Neural Networks',
                'total': int(3998 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(3998 * base_multiplier * 0.98 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(3998 * base_multiplier * 0.015 * np.random.uniform(0.5, 1.5)),
                'rejected': int(3998 * base_multiplier * 0.005 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'GLOBAL',
                'uptime': 99.99
            }
        ],
        'engines': [
            {
                'id': 'PE-SEPA-001',
                'name': 'SEPA Credit Transfer Engine',
                'type': 'ISO20022/SWIFT',
                'total': int(2156 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(2156 * base_multiplier * 0.98 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(2156 * base_multiplier * 0.015 * np.random.uniform(0.5, 1.5)),
                'rejected': int(2156 * base_multiplier * 0.005 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'EU',
                'uptime': 99.97
            },
            {
                'id': 'PE-SWIFT-002',
                'name': 'SWIFT International Engine',
                'type': 'MT/MX Messages',
                'total': int(1887 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(1887 * base_multiplier * 0.96 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(1887 * base_multiplier * 0.03 * np.random.uniform(0.5, 1.5)),
                'rejected': int(1887 * base_multiplier * 0.01 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'GLOBAL',
                'uptime': 99.85
            },
            {
                'id': 'PE-ACH-003',
                'name': 'ACH Processing Engine',
                'type': 'NACHA/CPA',
                'total': int(1654 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(1654 * base_multiplier * 0.97 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(1654 * base_multiplier * 0.02 * np.random.uniform(0.5, 1.5)),
                'rejected': int(1654 * base_multiplier * 0.01 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'AMERICAS',
                'uptime': 99.92
            },
            {
                'id': 'PE-RTP-004',
                'name': 'Real-time Payment Engine',
                'type': 'FedNow/RTP',
                'total': int(1432 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(1432 * base_multiplier * 0.99 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(1432 * base_multiplier * 0.008 * np.random.uniform(0.5, 1.5)),
                'rejected': int(1432 * base_multiplier * 0.002 * np.random.uniform(0.8, 1.2)),
                'status': 'healthy',
                'region': 'US',
                'uptime': 99.99
            },
            {
                'id': 'PE-CB-005',
                'name': 'Cross-border Corridors',
                'type': 'Multi-Rail',
                'total': int(876 * base_multiplier * np.random.uniform(0.9, 1.1)),
                'completed': int(876 * base_multiplier * 0.94 * np.random.uniform(0.98, 1.02)),
                'in_progress': int(876 * base_multiplier * 0.04 * np.random.uniform(0.5, 1.5)),
                'rejected': int(876 * base_multiplier * 0.02 * np.random.uniform(0.8, 1.2)),
                'status': 'warning',
                'region': 'GLOBAL',
                'uptime': 98.7
            }
        ]
    }

def display_professional_system_card(system, container):
    """Display a professional enterprise-grade system card"""
    with container:
        # Calculate metrics
        completion_rate = (system['completed'] / system['total'] * 100) if system['total'] > 0 else 0
        rejection_rate = (system['rejected'] / system['total'] * 100) if system['total'] > 0 else 0
        in_progress_rate = (system['in_progress'] / system['total'] * 100) if system['total'] > 0 else 0
        
        # Status configuration
        status_config = {
            'healthy': {'icon': '🟢', 'class': 'healthy', 'text': 'Operational'},
            'warning': {'icon': '🟡', 'class': 'warning', 'text': 'Degraded'},
            'error': {'icon': '🔴', 'class': 'error', 'text': 'Critical'}
        }
        
        status = status_config.get(system['status'], status_config['healthy'])
        
        # Create container with proper styling
        with st.container():
            # Add colored border based on status
            border_color = "#10b981" if system['status'] == 'healthy' else "#f59e0b" if system['status'] == 'warning' else "#ef4444"
            
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                border: 1px solid rgba(0,0,0,0.04);
                border-top: 4px solid {border_color};
                transition: all 0.3s ease;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <h3 style="margin: 0; font-size: 1.3rem; font-weight: 600; color: #1f2937; font-family: 'Inter', sans-serif;">{system['name']}</h3>
                        <span style="font-size: 0.85rem; color: #6b7280; background: #f3f4f6; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 500;">{system['id']}</span>
                    </div>
                    <span style="font-size: 1.8rem;">{status['icon']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Use Streamlit's native metrics in columns for better compatibility
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="💼 Total Transactions",
                    value=f"{system['total']:,}"
                )
                
                st.metric(
                    label="⏳ In Progress",
                    value=f"{system['in_progress']:,}",
                    delta=f"{in_progress_rate:.1f}%"
                )
            
            with col2:
                st.metric(
                    label="✅ Completed",
                    value=f"{system['completed']:,}",
                    delta=f"↗ {completion_rate:.1f}%"
                )
                
                st.metric(
                    label="❌ Rejected",
                    value=f"{system['rejected']:,}",
                    delta=f"↓ {rejection_rate:.1f}%",
                    delta_color="inverse"
                )
            
            # System details
            st.markdown(f"""
            <div style="
                font-size: 0.8rem; 
                color: #6b7280; 
                margin-top: 1rem; 
                padding-top: 1rem; 
                border-top: 1px solid #e5e7eb;
                background: #f8fafc;
                padding: 0.8rem;
                border-radius: 8px;
                margin-bottom: 1rem;
            ">
                <strong>Type:</strong> {system['type']} | <strong>Region:</strong> {system['region']} | <strong>Uptime:</strong> {system['uptime']}%
            </div>
            """, unsafe_allow_html=True)
        
        # Professional analytics button
        if st.button(
            f"🔍 Deep Analytics • {system['name']}", 
            key=f"analytics_{system['id']}",
            help=f"View comprehensive analytics for {system['name']}",
            type="secondary",
            use_container_width=True
        ):
            st.session_state.selected_system = system
            st.rerun()

def generate_professional_analytics_data(system_id, time_range='24h'):
    """Generate payment-focused analytics data"""
    
    if time_range == '24h':
        periods = 24
        freq = 'H'
        date_format = '%H:%M'
    elif time_range == '7d':
        periods = 7
        freq = 'D'
        date_format = '%m/%d'
    else:  # 30d
        periods = 30
        freq = 'D'
        date_format = '%m/%d'
    
    # Create realistic time series with business patterns
    if time_range == '30d':
        base_date = datetime.now() - timedelta(days=periods-1)
    elif time_range == '7d':
        base_date = datetime.now() - timedelta(days=periods-1)
    else:  # 24h
        base_date = datetime.now() - timedelta(hours=periods-1)
    
    dates = pd.date_range(base_date, periods=periods, freq=freq)
    
    # Generate realistic payment patterns
    data = []
    for i, date in enumerate(dates):
        # Business hours effect (higher volume during 9-17)
        if time_range == '24h':
            hour_factor = 1.8 if 9 <= date.hour <= 17 else 0.4
        else:
            hour_factor = 1.0
        
        # Day of week effect (lower on weekends)
        dow_factor = 0.3 if date.weekday() >= 5 else 1.0
        
        # Random variations
        random_factor = np.random.uniform(0.8, 1.2)
        
        # Base payment volume
        base_volume = 150 * hour_factor * dow_factor * random_factor
        payment_count = max(10, int(base_volume))
        
        # Average payment value varies by system type
        if 'SEPA' in system_id:
            avg_payment_value = np.random.uniform(2500, 15000)  # €2.5K - €15K
        elif 'SWIFT' in system_id:
            avg_payment_value = np.random.uniform(50000, 500000)  # €50K - €500K
        elif 'ACH' in system_id:
            avg_payment_value = np.random.uniform(1000, 8000)   # €1K - €8K
        elif 'RTP' in system_id:
            avg_payment_value = np.random.uniform(500, 5000)    # €500 - €5K
        else:
            avg_payment_value = np.random.uniform(5000, 25000)  # €5K - €25K
        
        total_value = payment_count * avg_payment_value
        
        # Processing time in business terms (end-to-end payment time)
        processing_time_minutes = max(1, np.random.normal(15, 8))  # 1-30 minutes typical
        
        # Business-relevant error rate
        error_rate = max(0, np.random.gamma(1.5, 0.8))  # 0-5% error rate
        
        # Success rate (business metric)
        success_rate = min(100, max(95, 100 - error_rate))
        
        data.append({
            'timestamp': date,
            'time_label': date.strftime(date_format),
            'payment_count': payment_count,
            'payment_value_eur': int(total_value),
            'avg_payment_value': int(avg_payment_value),
            'processing_time_minutes': processing_time_minutes,
            'error_rate_percent': error_rate,
            'success_rate_percent': success_rate,
            'failed_payments': int(payment_count * error_rate / 100),
            'successful_payments': payment_count - int(payment_count * error_rate / 100)
        })
    
    return pd.DataFrame(data)

def create_payment_focused_charts(df):
    """Create payment operations focused charts with clear business context"""
    
    # 1. Payment Volume Chart - Clear business context
    fig_volume = go.Figure()
    fig_volume.add_trace(go.Scatter(
        x=df['time_label'],
        y=df['payment_count'],
        mode='lines+markers',
        name='Payments Processed',
        line=dict(color='#667eea', width=3),
        marker=dict(size=6, color='#667eea'),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)',
        hovertemplate='<b>%{x}</b><br>Payments: %{y:,}<br><extra></extra>'
    ))
    fig_volume.update_layout(
        title=dict(
            text='Daily Payment Processing Volume<br><sub>Number of payments processed per hour/day</sub>', 
            font=dict(size=18, family='Inter')
        ),
        xaxis=dict(title='Time Period', gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(title='Number of Payments', gridcolor='rgba(0,0,0,0.1)'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        font=dict(family='Inter')
    )
    
    # 2. Payment Value Chart - Clear monetary context
    fig_value = go.Figure()
    fig_value.add_trace(go.Bar(
        x=df['time_label'],
        y=df['payment_value_eur'] / 1000000,  # Convert to millions
        name='Payment Value',
        marker_color='#10b981',
        hovertemplate='<b>%{x}</b><br>Value: €%{y:.1f}M<br><extra></extra>'
    ))
    fig_value.update_layout(
        title=dict(
            text='Daily Payment Value Processed<br><sub>Total monetary value of payments processed (€ Millions)</sub>', 
            font=dict(size=18, family='Inter')
        ),
        xaxis=dict(title='Time Period', gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(title='Payment Value (€ Millions)', gridcolor='rgba(0,0,0,0.1)'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        font=dict(family='Inter')
    )
    
    # 3. Success vs Failed Payments - Business outcome focus
    fig_success = go.Figure()
    fig_success.add_trace(go.Scatter(
        x=df['time_label'],
        y=df['successful_payments'],
        mode='lines+markers',
        name='Successful Payments',
        line=dict(color='#10b981', width=3),
        hovertemplate='<b>%{x}</b><br>Successful: %{y:,}<br><extra></extra>'
    ))
    fig_success.add_trace(go.Scatter(
        x=df['time_label'],
        y=df['failed_payments'],
        mode='lines+markers',
        name='Failed Payments',
        line=dict(color='#ef4444', width=3),
        hovertemplate='<b>%{x}</b><br>Failed: %{y:,}<br><extra></extra>'
    ))
    fig_success.update_layout(
        title=dict(
            text='Payment Success vs Failure Trends<br><sub>Tracking successful and failed payment counts over time</sub>', 
            font=dict(size=18, family='Inter')
        ),
        xaxis=dict(title='Time Period', gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(title='Number of Payments', gridcolor='rgba(0,0,0,0.1)'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        font=dict(family='Inter')
    )
    
    # 4. Average Payment Size - Business insight
    fig_avg_payment = go.Figure()
    fig_avg_payment.add_trace(go.Scatter(
        x=df['time_label'],
        y=df['avg_payment_value'] / 1000,  # Convert to thousands
        mode='lines+markers',
        name='Average Payment Size',
        line=dict(color='#8b5cf6', width=3),
        marker=dict(size=6),
        hovertemplate='<b>%{x}</b><br>Avg Payment: €%{y:.1f}K<br><extra></extra>'
    ))
    fig_avg_payment.update_layout(
        title=dict(
            text='Average Payment Size Trends<br><sub>Average monetary value per payment transaction (€ Thousands)</sub>', 
            font=dict(size=18, family='Inter')
        ),
        xaxis=dict(title='Time Period', gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(title='Average Payment Value (€ Thousands)', gridcolor='rgba(0,0,0,0.1)'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        font=dict(family='Inter')
    )
    
    return fig_volume, fig_value, fig_success, fig_avg_payment

def show_professional_analytics():
    """Show payment operations focused analytics dashboard"""
    system = st.session_state.selected_system
    
    # Professional header
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col1:
        if st.button("← Dashboard", type="primary", use_container_width=True):
            st.session_state.selected_system = None
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-header">
            <h1 class="dashboard-title">Payment Analytics: {system['name']}</h1>
            <p class="dashboard-subtitle">System ID: {system['id']} | Type: {system['type']} | Region: {system['region']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        time_range = st.selectbox("Time Range", ["24h", "7d", "30d"], key="analytics_time")
    
    # Generate payment analytics data
    df = generate_professional_analytics_data(system['id'], time_range)
    
    # Payment Operations KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Calculate daily totals
    total_payments_today = df['payment_count'].sum()
    total_value_today = df['payment_value_eur'].sum()
    avg_payment_size = df['avg_payment_value'].mean()
    success_rate = df['success_rate_percent'].mean()
    total_failed = df['failed_payments'].sum()
    
    payment_kpis = [
        ("Daily Payment Count", f"{total_payments_today:,}", "#3b82f6"),
        ("Daily Payment Value", f"€{total_value_today/1000000:.1f}M", "#10b981"),
        ("Average Payment Size", f"€{avg_payment_size/1000:.1f}K", "#8b5cf6"),
        ("Success Rate", f"{success_rate:.1f}%", "#059669"),
        ("Failed Payments", f"{total_failed:,}", "#ef4444")
    ]
    
    for i, (label, value, color) in enumerate(payment_kpis):
        with [col1, col2, col3, col4, col5][i]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {color};">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Payment Operations Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Payment Volume & Value", "✅ Success & Failure Analysis", "📈 Business Insights"])
    
    with tab1:
        st.markdown("#### Payment Processing Overview")
        
        # Create charts
        fig_volume, fig_value, fig_success, fig_avg_payment = create_payment_focused_charts(df)
        
        # Payment count chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_volume, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Payment value chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_value, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Daily summary table
        st.markdown("#### Daily Summary")
        if time_range == "7d" or time_range == "30d":
            daily_summary = df.groupby(df['time_label']).agg({
                'payment_count': 'sum',
                'payment_value_eur': 'sum',
                'successful_payments': 'sum',
                'failed_payments': 'sum'
            }).round(0)
            daily_summary['payment_value_eur'] = daily_summary['payment_value_eur'] / 1000000  # Convert to millions
            daily_summary.columns = ['Total Payments', 'Value (€M)', 'Successful', 'Failed']
            st.dataframe(daily_summary, use_container_width=True)
    
    with tab2:
        st.markdown("#### Payment Success & Failure Tracking")
        
        # Success vs failure chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_success, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Success rate metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Overall Performance")
            st.metric("Success Rate", f"{success_rate:.2f}%")
            st.metric("Total Successful", f"{df['successful_payments'].sum():,}")
            st.metric("Total Failed", f"{df['failed_payments'].sum():,}")
        
        with col2:
            st.markdown("#### Processing Times")
            avg_processing = df['processing_time_minutes'].mean()
            max_processing = df['processing_time_minutes'].max()
            st.metric("Average Processing Time", f"{avg_processing:.1f} min")
            st.metric("Maximum Processing Time", f"{max_processing:.1f} min")
            
            # SLA compliance (assuming 30 min SLA)
            sla_compliance = (df['processing_time_minutes'] <= 30).mean() * 100
            st.metric("SLA Compliance (30min)", f"{sla_compliance:.1f}%")
        
        with col3:
            st.markdown("#### Error Analysis")
            avg_error_rate = df['error_rate_percent'].mean()
            max_error_rate = df['error_rate_percent'].max()
            st.metric("Average Error Rate", f"{avg_error_rate:.2f}%")
            st.metric("Peak Error Rate", f"{max_error_rate:.2f}%")
            
            # Calculate improvement/degradation
            if len(df) >= 2:
                recent_error = df['error_rate_percent'].tail(3).mean()
                earlier_error = df['error_rate_percent'].head(3).mean()
                trend = "↗ Improving" if recent_error < earlier_error else "↘ Degrading"
                st.metric("Error Rate Trend", trend)
    
    with tab3:
        st.markdown("#### Business Intelligence & Insights")
        
        # Average payment size chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_avg_payment, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Business insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Payment Pattern Analysis")
            
            # Peak payment analysis
            peak_hour = df.loc[df['payment_count'].idxmax()]
            st.info(f"**Peak Processing Hour:** {peak_hour['time_label']} with {peak_hour['payment_count']:,} payments")
            
            # Value concentration
            high_value_periods = df[df['payment_value_eur'] > df['payment_value_eur'].quantile(0.8)]
            st.info(f"**High Value Periods:** {len(high_value_periods)} time periods with >80th percentile value")
            
            # Processing efficiency
            efficient_periods = df[df['processing_time_minutes'] < df['processing_time_minutes'].median()]
            efficiency_rate = len(efficient_periods) / len(df) * 100
            st.info(f"**Processing Efficiency:** {efficiency_rate:.0f}% of periods below median processing time")
        
        with col2:
            st.markdown("#### Operational Recommendations")
            
            # Generate business recommendations
            if avg_error_rate > 3:
                st.warning("⚠️ **High Error Rate**: Consider reviewing validation rules or system capacity")
            else:
                st.success("✅ **Error Rate**: Within acceptable range")
            
            if avg_processing > 20:
                st.warning("⚠️ **Processing Time**: Above optimal range, investigate bottlenecks")
            else:
                st.success("✅ **Processing Time**: Within optimal range")
            
            if success_rate < 95:
                st.error("🚨 **Success Rate**: Below target, immediate attention required")
            else:
                st.success("✅ **Success Rate**: Meeting business targets")
            
            # Capacity utilization
            peak_capacity = df['payment_count'].max()
            avg_capacity = df['payment_count'].mean()
            utilization = (avg_capacity / peak_capacity) * 100
            
            if utilization > 80:
                st.warning(f"⚠️ **Capacity**: {utilization:.0f}% average utilization - consider scaling")
            else:
                st.info(f"ℹ️ **Capacity**: {utilization:.0f}% average utilization - healthy range")

def main():
    # Professional header
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">Enterprise Payment Processing Hub</h1>
        <p class="dashboard-subtitle">Real-time operational intelligence across global payment infrastructure</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for detailed analytics view
    if st.session_state.selected_system:
        show_professional_analytics()
        return
    
    # Professional sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("🎛️ Operations Control")
        
        # Time range with professional styling
        time_range = st.selectbox(
            "⏱️ Monitoring Window",
            ["Last 15 minutes", "Last 30 minutes", "Last 1 hour", "Last 4 hours", "Last 24 hours"],
            index=2
        )
        
        # Auto-refresh toggle
        auto_refresh = st.toggle("🔄 Auto-refresh", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
        
        if auto_refresh:
            refresh_rate = st.slider("Refresh Rate (seconds)", 10, 60, 30)
        
        # Manual refresh
        if st.button("⚡ Refresh Now", type="primary", use_container_width=True):
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        # Payment operations overview
        st.markdown("---")
        st.markdown("#### 📊 Payment Systems Status")
        systems_data = create_enterprise_sample_data()
        
        # Count systems by status
        healthy_count = sum(1 for category in systems_data.values() for system in category if system['status'] == 'healthy')
        warning_count = sum(1 for category in systems_data.values() for system in category if system['status'] == 'warning')
        error_count = sum(1 for category in systems_data.values() for system in category if system['status'] == 'error')
        
        st.metric("🟢 Healthy Systems", healthy_count)
        st.metric("🟡 Systems with Warnings", warning_count)
        if error_count > 0:
            st.metric("🔴 Critical Systems", error_count)
        
        # Payment volume summary
        st.markdown("#### 💰 Today's Volume")
        total_volume = sum(s['total'] for category in systems_data.values() for s in category)
        successful_volume = sum(s['completed'] for category in systems_data.values() for s in category)
        success_rate = (successful_volume / total_volume * 100) if total_volume > 0 else 0
        
        st.metric("Total Payments", f"{total_volume:,}")
        st.metric("Success Rate", f"{success_rate:.1f}%")
        
        # Regional payment status
        st.markdown("#### 🌍 Regional Operations")
        regions = set()
        region_status = {}
        for category in systems_data.values():
            for system in category:
                region = system['region']
                regions.add(region)
                if region not in region_status:
                    region_status[region] = []
                region_status[region].append(system['status'])
        
        for region in sorted(regions):
            statuses = region_status[region]
            if 'error' in statuses:
                st.error(f"{region}: Critical Issues")
            elif 'warning' in statuses:
                st.warning(f"{region}: Minor Issues")
            else:
                st.success(f"{region}: Operational")
        
        # Quick actions
        st.markdown("---")
        st.markdown("#### ⚡ Quick Actions")
        if st.button("📈 Export Daily Report", use_container_width=True):
            st.success("Daily report exported successfully!")
        
        if st.button("🔔 View Alerts", use_container_width=True):
            st.info("No active alerts")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate enterprise data
    systems_data = create_enterprise_sample_data()
    
    # Professional system sections
    sections = [
        ("🔄 Channel Systems", systems_data['channels'], "Payment ingestion and customer-facing interfaces"),
        ("⚙️ Processing Middleware", systems_data['preprocessors'], "Validation, compliance, and risk management"),
        ("🏭 Payment Engines", systems_data['engines'], "Core payment processing and settlement")
    ]
    
    for section_title, systems, description in sections:
        st.markdown(f'<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<h2 class="section-header">{section_title}</h2>', unsafe_allow_html=True)
        st.markdown(f"*{description}*")
        
        # Display systems in a professional grid
        cols = st.columns(min(3, len(systems)))
        for i, system in enumerate(systems):
            display_professional_system_card(system, cols[i % len(cols)])
    
    # Auto-refresh mechanism
    if st.session_state.auto_refresh:
        time.sleep(1)  # Small delay to prevent excessive refreshing
        st.rerun()

if __name__ == "__main__":
    main()
