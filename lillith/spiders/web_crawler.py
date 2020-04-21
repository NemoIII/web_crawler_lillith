# -*- coding: utf-8 -*-
import scrapy


class PcSpider(scrapy.Spider):
	name = 'web_crawler'
	"""
		- allowed_domains:
			Host que é permitido fazer a busca
		- start_urls:
			Domínio e o local onde irá realizar a busca.
	"""
	allowed_domains = ['olx.com.br']
	start_urls = ['https://www.olx.com.br/computadores-e-acessorios']

	
	"""
		Função que realiza a busca.
		- pcs:
			Caminho que irá realizar na página de destino, ignorando as propagandas.
			Que a exemplo é a parte do código '/li[not(contains(@class, "list_native"))]'
		- prox:
			Realiza a passada para a página seguinte no domínio.
	"""
	def parse(self, response):
		pcs = response.xpath('//ul[@id="main-ad-list"]/li[not(contains(@class, "list_native"))]')
		for pc in pcs:
			links = pc.xpath('./a/@href').extract_first()
			yield scrapy.Request(url=links,callback=self.cb)
		prox = response.xpath('//li[contains(@class, "item next")]//a[@rel = "next"]/@href').extract_first()
		if prox:
			self.log(f"Próxima Página: {prox}")
			yield scrapy.Request(url=prox, callback=self.parse)

	"""
		Função que define o que é buscado.
		- titulo:
			Pega a parte onde tem o título, com o intúito de identificar o que é buscado na página.
		- custo:
			Busca apresentar o valor, que nesse caso, são dos anúncios da olx.
	"""
	def cb(self,response):
		titulo = response.xpath('//title/text()').extract_first()
		custo = response.xpath('//*[contains(@class, "actual-price")]/text()').extract_first()
		yield {'titulo': titulo, 'custo': custo}