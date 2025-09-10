from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
import io
import os
import html
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

@app.route('/')
def index():
    """Page d'accueil avec le formulaire"""
    return render_template('index.html')

def process_text_for_pdf(text):
    """Traite le texte pour un meilleur rendu PDF en préservant les paragraphes"""
    # Échapper les caractères HTML spéciaux pour éviter les erreurs de parsing
    text = html.escape(text)
    
    # Diviser le texte en paragraphes (séparer par double saut de ligne ou simple)
    paragraphs = re.split(r'\n\s*\n', text)
    
    processed_paragraphs = []
    for para in paragraphs:
        # Nettoyer le paragraphe et remplacer les sauts de ligne simples par des espaces
        # sauf si c'est clairement une liste ou des éléments structurés
        para = para.strip()
        if para:
            # Détecter si c'est une liste (commence par -, *, nombre, etc.)
            lines = para.split('\n')
            if any(re.match(r'^\s*[-*•]\s+', line) or re.match(r'^\s*\d+\.\s+', line) for line in lines):
                # C'est une liste, préserver les sauts de ligne
                para = para.replace('\n', '<br/>')
            else:
                # Texte normal, joindre les lignes avec des espaces
                para = ' '.join(line.strip() for line in lines if line.strip())
            processed_paragraphs.append(para)
    
    return processed_paragraphs

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """Génère un PDF à partir du texte soumis"""
    text = request.form.get('text', '').strip()
    
    if not text:
        flash('Veuillez saisir du texte avant de générer le PDF.')
        return redirect(url_for('index'))
    
    try:
        # Créer un buffer en mémoire pour le PDF
        buffer = io.BytesIO()
        
        # Créer le PDF avec reportlab - marges améliorées
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=72)
        
        # Styles pour le texte améliorés
        styles = getSampleStyleSheet()
        
        # Créer un style personnalisé pour un meilleur rendu
        custom_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,  # Interligne
            spaceAfter=12,
            alignment=TA_LEFT,
            allowWidows=1,  # Éviter les lignes orphelines
            allowOrphans=1,
        )
        
        story = []
        
        # Traiter le texte pour préserver la structure
        processed_paragraphs = process_text_for_pdf(text)
        
        for i, paragraph_text in enumerate(processed_paragraphs):
            if paragraph_text.strip():
                # Utiliser Paragraph au lieu de Preformatted pour un meilleur rendu
                para = Paragraph(paragraph_text, custom_style)
                story.append(para)
                
                # Espacement entre les paragraphes (sauf pour le dernier)
                if i < len(processed_paragraphs) - 1:
                    story.append(Spacer(1, 6))
        
        # Construire le PDF
        doc.build(story)
        
        # Remettre le pointeur au début du buffer
        buffer.seek(0)
        
        # Retourner le fichier PDF en téléchargement
        return send_file(buffer, 
                        as_attachment=True, 
                        download_name='texte.pdf',
                        mimetype='application/pdf')
    
    except Exception as e:
        flash(f'Erreur lors de la génération du PDF: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Configuration flexible pour développement et déploiement
    # Replit utilise le port 5000, Render utilise la variable PORT (défaut 10000)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)