"""PDF report generation for Growth Leak Score Analyzer."""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from io import BytesIO
from models import AnalysisResult


def get_score_color(score: float) -> colors.Color:
    """Return color based on score range."""
    if score < 40:
        return colors.HexColor('#ff4444')  # Red
    elif score < 70:
        return colors.HexColor('#ffaa00')  # Orange
    else:
        return colors.HexColor('#44aa44')  # Green


def generate_pdf_report(result: AnalysisResult, website_url: str, business_info: dict) -> BytesIO:
    """
    Generate a professional PDF report of the Growth Leak Analysis.
    
    Args:
        result: AnalysisResult object with scores and recommendations
        website_url: The analyzed website URL
        business_info: Dictionary with questionnaire answers
        
    Returns:
        BytesIO buffer containing the PDF
    """
    # Create PDF buffer
    buffer = BytesIO()
    
    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#374151'),
        spaceAfter=8,
        leading=14,
    )
    
    # Title
    elements.append(Paragraph("📊 Growth Leak Score Analysis", title_style))
    elements.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        subtitle_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Website Info Box
    website_data = [
        ['Website Analyzed:', website_url],
        ['Industry:', business_info.get('industry', 'N/A')],
        ['Customer Value:', f"${business_info.get('avg_customer_value', 'N/A')}"],
        ['Main Channel:', business_info.get('main_channel', 'N/A')],
    ]
    
    website_table = Table(website_data, colWidths=[2*inch, 4.5*inch])
    website_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
    ]))
    elements.append(website_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Overall Score - Clean, centered display
    score_color = get_score_color(result.total_score)
    
    # Create centered score with proper spacing
    score_style = ParagraphStyle(
        'ScoreStyle',
        parent=body_style,
        alignment=TA_CENTER,
        leading=72,  # Line height
        spaceBefore=10,
        spaceAfter=10,
    )
    
    score_text = f'<font size="72" color="{score_color.hexval()}"><b>{result.total_score:.0f}</b></font><font size="36" color="#9ca3af">/100</font>'
    score_para = Paragraph(score_text, score_style)
    
    score_data = [[score_para]]
    
    score_table = Table(score_data, colWidths=[6.5*inch], rowHeights=[1.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 3, score_color),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(score_table)
    
    # Score interpretation
    if result.total_score >= 70:
        interpretation = "✅ <b>Strong Foundation</b> - Your website and marketing are performing well!"
        interp_color = colors.HexColor('#44aa44')
    elif result.total_score >= 40:
        interpretation = "⚠️ <b>Room for Improvement</b> - Some key areas need attention"
        interp_color = colors.HexColor('#ffaa00')
    else:
        interpretation = "🚨 <b>Critical Issues</b> - Significant growth opportunities are being missed"
        interp_color = colors.HexColor('#ff4444')
    
    interp_style = ParagraphStyle(
        'InterpStyle',
        parent=body_style,
        alignment=TA_CENTER,
        fontSize=12,
        textColor=interp_color,
    )
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(interpretation, interp_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Category Breakdown
    elements.append(Paragraph("📊 Category Breakdown", heading_style))
    
    # Create table data with proper wrapping
    category_data = [['Category', 'Score', 'Max', '%', 'Reasoning']]
    
    for cat in result.categories:
        percentage = (cat.score / cat.max_score * 100) if cat.max_score > 0 else 0
        
        # Color code the percentage
        if percentage >= 80:
            perc_color = '#44aa44'
        elif percentage >= 60:
            perc_color = '#ffaa00'
        else:
            perc_color = '#ff4444'
        
        # Wrap category name and reasoning in Paragraphs for proper text wrapping
        cat_name_para = Paragraph(cat.name, ParagraphStyle('CatName', parent=body_style, fontSize=8, fontName='Helvetica-Bold'))
        reasoning_para = Paragraph(cat.reasoning, ParagraphStyle('Reasoning', parent=body_style, fontSize=7, leading=9))
        
        category_data.append([
            cat_name_para,
            f"{cat.score:.1f}",
            f"{cat.max_score:.1f}",
            Paragraph(f"<font color='{perc_color}'><b>{percentage:.0f}%</b></font>", 
                     ParagraphStyle('Perc', parent=body_style, fontSize=8, alignment=TA_CENTER)),
            reasoning_para
        ])
    
    category_table = Table(
        category_data,
        colWidths=[1.6*inch, 0.5*inch, 0.5*inch, 0.5*inch, 3.4*inch]
    )
    
    category_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        
        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
        ('FONTSIZE', (1, 1), (3, -1), 8),
        ('ALIGN', (1, 1), (3, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (4, 1), (4, -1), 'LEFT'),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Top alignment for better text flow
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        
        # Padding - increased for wrapped text
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(category_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Biggest Growth Leak
    elements.append(Paragraph("🚨 Your Biggest Growth Leak", heading_style))
    
    leak_cat = next(c for c in result.categories if c.name == result.biggest_leak_category)
    leak_percentage = (leak_cat.score / leak_cat.max_score * 100) if leak_cat.max_score > 0 else 0
    
    leak_data = [[
        Paragraph(f"<b>{result.biggest_leak_category}</b>", body_style),
        Paragraph(
            f"<font color='#ff4444'><b>{leak_cat.score:.1f}/{leak_cat.max_score} ({leak_percentage:.0f}%)</b></font>",
            ParagraphStyle('LeakScore', parent=body_style, alignment=TA_RIGHT)
        )
    ], [
        Paragraph(leak_cat.reasoning, body_style),
        ''
    ]]
    
    leak_table = Table(leak_data, colWidths=[5*inch, 1.5*inch])
    leak_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef2f2')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#ff4444')),
        ('SPAN', (0, 1), (-1, 1)),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(leak_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Recommendation
    elements.append(Paragraph("💡 Recommended Next Step", heading_style))
    
    reco_para = Paragraph(result.recommendation, body_style)
    reco_data = [[reco_para]]
    
    reco_table = Table(reco_data, colWidths=[6.5*inch])
    reco_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#3b82f6')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(reco_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=body_style,
        fontSize=8,
        textColor=colors.HexColor('#9ca3af'),
        alignment=TA_CENTER,
    )
    
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(
        "Growth Leak Score Analyzer • Powered by AI",
        footer_style
    ))
    elements.append(Paragraph(
        f"Report generated on {datetime.now().strftime('%B %d, %Y')}",
        footer_style
    ))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF from buffer
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    # Test PDF generation
    from models import CategoryScore, AnalysisResult
    
    print("Testing PDF generation...")
    
    # Create sample data
    test_categories = [
        CategoryScore(
            name="Value Proposition Clarity",
            score=12.0,
            max_score=15.0,
            reasoning="Clear headline and messaging, but could be more specific"
        ),
        CategoryScore(
            name="Call-to-Action Strength",
            score=10.0,
            max_score=15.0,
            reasoning="Primary CTA is visible but not prominent enough"
        ),
        CategoryScore(
            name="Lead Capture Mechanism",
            score=8.0,
            max_score=15.0,
            reasoning="Contact form present but missing live chat"
        ),
        CategoryScore(
            name="Trust & Social Proof",
            score=5.0,
            max_score=10.0,
            reasoning="Some testimonials but no case studies or logos"
        ),
        CategoryScore(
            name="SEO & Content Basics",
            score=7.0,
            max_score=10.0,
            reasoning="Good meta tags, blog present but infrequent posts"
        ),
        CategoryScore(
            name="Tracking & Follow-up Readiness",
            score=8.0,
            max_score=10.0,
            reasoning="Google Analytics detected, no retargeting pixels"
        ),
        CategoryScore(
            name="Marketing Channel Effectiveness",
            score=7.0,
            max_score=12.0,
            reasoning="Single-channel dependence creates risk"
        ),
        CategoryScore(
            name="Conversion Health",
            score=8.0,
            max_score=13.0,
            reasoning="Conversion rate below industry average"
        ),
    ]
    
    test_result = AnalysisResult(
        categories=test_categories,
        total_score=65.0,
        biggest_leak_category="Lead Capture Mechanism",
        recommendation="Add a live chat widget to your website homepage. This will provide visitors with immediate support and increase lead capture by an estimated 20-30%."
    )
    
    test_business_info = {
        'industry': 'B2B SaaS',
        'avg_customer_value': 5000,
        'main_channel': 'LinkedIn Ads',
        'monthly_traffic': '2,000',
        'conversion_rate': '1.5%',
    }
    
    # Generate PDF
    try:
        pdf_buffer = generate_pdf_report(
            test_result,
            "https://www.example.com",
            test_business_info
        )
        
        # Save to file
        with open("test_report.pdf", "wb") as f:
            f.write(pdf_buffer.getvalue())
        
        print("✅ PDF generated successfully: test_report.pdf")
        print(f"   File size: {len(pdf_buffer.getvalue())} bytes")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
