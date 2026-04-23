import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    # Base HTML structure with premium card look
    html = f"""
    <div style="background: white; padding: 25px; border-radius: 20px; border: 1px solid #6c757d; margin-bottom: 0px; position: relative; z-index: 1;">
        <h3 style="margin: 0; color: #2F3136; font-size: 1.6rem; font-family: 'Outfit', sans-serif; font-weight: 700;">{name}</h3>
        <p style="color: #64748b; margin: 15px 0; font-family: 'Outfit', sans-serif; font-size: 1rem;">
            Code : <span style="background: #E0E3FF; color: #5865F2; padding: 4px 10px; border-radius: 8px; font-weight: 600;">{code}</span> <span style="color: #cbd5e1; margin: 0 5px;">|</span> Section : <span style="color: #64748b; font-weight: 600;">{section}</span>
        </p>
    """
    
    if stats:
        html += '<div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 15px;">'
        for icon, label, value in stats:
            bg_color = "#E0E3FF" if "Student" in label else "#FFF0F5"
            text_color = "#5865F2" if "Student" in label else "#2F3136"
            html += f"""<div style="background: {bg_color}; padding: 6px 12px; border-radius: 10px; font-size: 0.95rem; font-family: 'Outfit', sans-serif; font-weight: 600; display: flex; align-items: center; gap: 6px;">{icon} <span style="color: {text_color};">{value} {label}</span></div>"""
        html += '</div>'
        
    html += "</div>"
    
    # Render the card
    st.markdown(html, unsafe_allow_html=True)
    
    # If there's a callback for buttons (Streamlit buttons cannot be inside st.markdown HTML)
    if footer_callback:
        footer_callback()