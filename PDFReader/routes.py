import os
import PyPDF2
import matplotlib.pyplot as plt
import io
import gzip
import urllib, base64
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from flask import render_template,redirect,flash,redirect,url_for,session
from PDFReader import app
from PDFReader.forms import InputForm


@app.route('/',methods=['GET','POST'])
def Home():
	uri=''
	form=InputForm()
	if form.validate_on_submit():
		if form.PDF.data:
			pdfFileObj = form.PDF.data
			pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
			N=pdfReader.numPages
			Pages_Count=''
			for inti in range (0,N):
				List2=[]
				Listfin=[]
				pageObj = pdfReader.getPage(inti)
				pages=pageObj.extractText()
				Pages_Count=Pages_Count+pages
			pdfFileObj.close()
			dataset = Pages_Count
			dataset = dataset.lower()
			dataset=bytes(dataset, 'utf-8')
			dataset=gzip.compress(dataset)
			session['my_var'] = dataset
			return redirect(url_for('results'))
	return render_template('home.html',title='PDF Reader-Home',form=form)


@app.route('/results',methods=['GET','POST'])
def results():
	dataset = session.get('my_var', None)
	dataset = gzip.decompress(dataset)
	dataset=dataset.decode("utf-8")
	if dataset:
		cloud = WordCloud(background_color = "black", max_words = 200, stopwords = set(STOPWORDS))
		wordclouds=cloud.generate(dataset)
		plt.figure(figsize=(4.8,2.7))
		plt.imshow(wordclouds, interpolation="bilinear")
		plt.axis('off')
		fig = plt.gcf()
		buf = io.BytesIO()
		fig.savefig(buf, format='png')
		buf.seek(0)
		base = base64.b64encode(buf.read())
		uri = 'data:image/png;base64,' + urllib.parse.quote(base)
		return render_template('results.html',title='PDF Reader-Results',img=uri)
	else:
		return redirect(url_for('Home'))