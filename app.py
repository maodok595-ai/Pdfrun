from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted, Spacer
from reportlab.lib.enums import TA_LEFT
import io
import os
from xml.sax.saxutils import escape

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

@app.route('/')
def index():
    """Page d'accueil avec le formulaire"""
    return render_template('index.html')

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
        
        # Créer le PDF avec reportlab
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Styles pour le texte
        styles = getSampleStyleSheet()
        story = []
        
        # Diviser le texte en paragraphes
        paragraphs = text.split('\n')
        
        for paragraph_text in paragraphs:
            if paragraph_text.strip():
                # Utiliser Preformatted pour éviter les problèmes avec les caractères spéciaux
                para = Preformatted(paragraph_text.strip(), styles['Normal'])
                story.append(para)
                story.append(Spacer(1, 12))
        
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
    # Utiliser debug=False en production pour la sécurité
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)