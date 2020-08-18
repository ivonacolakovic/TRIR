import scrapy

class WorldFactBookSpider(scrapy.Spider):
    name = 'worldfactbook'

    allowed_domains = ['cia.gov']
    main_url = 'https://www.cia.gov/library/publications/the-world-factbook/'
    parsedCountries = {}

    def start_requests(self):
        urls = []
        urls.append(self.main_url)

        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_main_page)

    def parse_main_page(self, response):
        worldCountries = response.css('select#search-place option::attr("value")').extract()

        for country_url in worldCountries:
            if country_url and country_url != "geos/xx.html":
                yield scrapy.Request(self.main_url + country_url, callback=self.parse_country_details)

    def parse_country_details(self, response):
        background = response.css('div#field-background div.category_data.subfield::text').extract_first()
        countryName = response.css('div#geos_title span.region_name1.countryName::text').extract_first()
        meanElevation = response.css('div#field-elevation span.subfield-number::text').extract_first()
        agriculturalLandUse = response.css('div#field-land-use span.subfield-number::text').extract_first()

        totalDependencyRatio = response.css('div#field-dependency-ratios span.subfield-number::text').extract_first()
        medianAge = response.css('div#field-median-age span.subfield-number::text').extract_first()
        populationGrowthRate = response.css('div#field-population-growth-rate span.subfield-number::text').extract_first()
        birthRate = response.css('div#field-birth-rate span.subfield-number::text').extract_first()
        deathRate = response.css('div#field-death-rate span.subfield-number::text').extract_first()
        netMigrationRate = response.css('div#field-net-migration-rate span.subfield-number::text').extract_first()

        urbanization = response.css('div#field-urbanization span.subfield-number::text').extract()
        urbanPopulation = urbanization[0] if len(urbanization) > 0 else None
        rateOfUrbanization = urbanization[1] if len(urbanization) > 1 else None
        sexRatio = response.css('div#field-sex-ratio div.category_data.subfield:contains("total population:") span.subfield-number::text').extract_first()


        # self.parsedCountries[response.url[-7:]] = {
        countryData = {
            "Country": countryName,
            "Background": background.replace("\n", "").strip(),
            "Mean elevation (m)": float(meanElevation.replace(" m", "").replace(",", ".")) if meanElevation else None,
            "Agricultural land use (%)": float(agriculturalLandUse.replace("%", "")) if agriculturalLandUse else None,
            "Total dependency ratio": float(totalDependencyRatio) if totalDependencyRatio else None,
            "Median age": float(medianAge.replace(" years", "")) if medianAge else None,
            "Population growth rate (%)": float(populationGrowthRate.replace("%", "")) if populationGrowthRate else None,
            "Birth rate (births/1000 population)": float(birthRate.replace(" births/1,000 population", "")) if birthRate else None,
            "Death rate (deaths/1000 population)": float(deathRate.replace(" deaths/1,000 population", "")) if deathRate else None,
            "Net migration rate (migrants/1000 population)": float(netMigrationRate.replace(" migrant(s)/1,000 population", "")) if netMigrationRate else None,
            "Urban population (%)": float(urbanPopulation.replace("% of total population", "")) if urbanPopulation else None,
            "Rate of urbanization (%)": float(rateOfUrbanization.replace("% annual rate of change", "")) if rateOfUrbanization else None,
            "Sex ratio (male/female)": float(sexRatio.replace(" male(s)/female", "")) if sexRatio else None
        }

        yield countryData