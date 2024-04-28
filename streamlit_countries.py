# load up the libraries
import panel as pn
import pandas as pd
import altair as alt
import json
import numpy as np
import streamlit as st
import geopandas as gpd

pisa_df = pd.read_csv('PISA_data.csv')
country_codes = pd.read_csv('country_codes.csv')
pisa_df = pisa_df.merge(country_codes, left_on='country', right_on='code')
pisa_df['name'] = pisa_df['country_name']
pisa_df['time'] = pisa_df['time'].astype(int)


pisa_total = pisa_df[pisa_df['sex'] == 'TOT']
pisa_total = pisa_total.drop(columns=['country','index_code'])
pisa_total['name'] = pisa_total['country_name']
pisa_total['time'] = pisa_total['time'].astype(int)
pisa_total['rating_bins'] = pd.qcut(pisa_total['rating'], q= [0, 0.2, 0.4, 0.6, 0.8, 1], labels=['Very Low', 'Low', 'Medium','High', 'Very High'])

pisa_total['rating_bins_num'] = pd.qcut(pisa_total['rating'], q= [0, 0.2, 0.4, 0.6, 0.8, 1], labels=[5, 4, 3, 2, 1])



st.title('What is Standardized Testing Telling Us About Student Performance?')
st.header('By: Bella Karduck and Rosalie Morrissey', divider='grey')
st.write('Link to our website: https://si649-final-bella-rosalie.streamlit.app/')
st.write('Link to our GitHub: https://github.com/bkarduck/si649_final_proj')
st.header('Unwrapping and breaking down PISA scores to determine what leads to high student performance.', divider=False)
st.write("Standardized testing has become ubiquitous in the American K-12 schooling experience. First introduced in the mid-1800s, college entrance exams were introduced in the early 1900s. In today’s world, we often use standardized assessments to measure student achievement and teacher effectiveness. However, they were initially designed to measure student’s abilities with the ongoing trend of quantifying intelligence at the time. In the US, the “No Child Left Behind” policy accelerated standardized testing and increased it from secondary students to all grade school students. As a part of the policy, schools would be punished if their testing scores did not show improvement. The policy ended in 2015 and was replaced with the “Every Student Succeeds Act,” which gave states and individual families more control over determining the standards students should be held to.")

st.write("International standardized testing emerged in 1997 when the Organization for Economic Co-operation and Development (OECD) launched the Programme for International Student Assessment (PISA). The test is taken by 15-year-olds and looks at performance in reading, science, and mathematics every three years. The first test was administered in 2000, and the most recent was conducted in 2022. Due to the timing and availability of the 2022 data, it will not be analyzed in this article.")

st.write("While many European and North American countries have been taking the PISA since its inception, countries in South America have also begun to administer the assessment. From Asia, South Korea and Japan have long participated in the evaluation, yet very little data is available for the vast majority of the continent.")

st.subheader('See combined PISA (averages of reading, science, and mathematics) performance throughout the years through the slider:')
st.subheader('Visualization 1: Global Performance on PISA Over Time')


url_geojson = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_0_countries.geojson"
data_url_geojson = alt.Data(url=url_geojson, format=alt.DataFormat(property="features"))




year_options=list(pisa_total["time"].unique())
year_options=list(map(lambda x:int(x),year_options))
year_options.sort()



yearSelector = alt.selection_interval()


values = st.slider(
    'Select a year',
   min_value=2003, max_value=2018, value=2003, step=3)

# st.write('year selected:', values)

pisa_filtered2 = pisa_total[pisa_total['time'] == values]


axis_labels = (
    'datum.label == 1 ? "Very High" : datum.label == 2 ? "High" : datum.label == 3 ? "Medium" : datum.label == 4 ? "Low" : "Very Low"')


eu_chart = alt.Chart(data_url_geojson,title='Europe').mark_geoshape(stroke='white').transform_filter(
        alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Europe', ])
    ).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating",'rating_bins_num', 'rating_bins']),
    ).transform_filter(
    'isValid(datum.rating_bins_num)'
).encode(
        fill=alt.Color(
            "rating_bins_num:O",
            scale=alt.Scale(scheme="reds", reverse=True),
            sort = 'descending',
            legend=alt.Legend(title='Average PISA Scores', labelExpr=axis_labels),
            # ignore null

        ), 
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).properties(width=400, height=250).project(
type='mercator', reflectY=False, scale=150, translate=[150, 300])

eu_base = alt.Chart(data_url_geojson).mark_geoshape( fill='#666666',
    stroke='white').encode(tooltip=[alt.Tooltip("properties.name:N", title="Country")]).transform_filter(
        alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Europe', ])
    ).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating", 'rating_bins']),
    ).properties(width=400, height=250).project(
type='mercator', reflectY=False, scale=150, translate=[150, 300])


na_chart =alt.Chart(data_url_geojson, title='North America').mark_geoshape(stroke='white').transform_filter(
        alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Americas', ])
    ).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['North America', ])).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating", 'rating_bins_num', 'rating_bins']),
    ).transform_filter(
    'isValid(datum.rating_bins_num)'
).encode(
        fill=alt.Color(
            "rating_bins_num:O",
            scale=alt.Scale(scheme="reds", reverse=True),
      
            legend=alt.Legend(title='Average PISA Scores', labelExpr=axis_labels),
        ), 
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).properties(width=400, height=250)

na_base = alt.Chart(data_url_geojson).mark_geoshape(    fill='#666666',
    stroke='white').encode(tooltip=[alt.Tooltip("properties.name:N", title="Country")]).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['North America', ])).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating",'rating_bins'])).properties(width=400, height=250)

sa_chart = alt.Chart(data_url_geojson, title='South America').mark_geoshape(stroke='white').transform_filter(alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Americas', ])
    ).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['South America', ])).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating", 'rating_bins', 'rating_bins_num']),
    ).transform_filter(
    'isValid(datum.rating_bins_num)'
).encode(
        fill=alt.Color(
            "rating_bins_num:O",
            scale=alt.Scale(scheme="reds", reverse=True),
        
            legend=alt.Legend(title='Average PISA Scores', labelExpr=axis_labels),
        ), 
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).properties(width=400, height=250).project(
type='mercator', reflectY=False, scale=170, translate=[400, 50])


sa_base = alt.Chart(data_url_geojson).mark_geoshape( fill='#666666',
    stroke='white').encode(tooltip=[
            alt.Tooltip("properties.name:N", title="Country")]).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['South America', ])).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating",'rating_bins'])).properties(width=400, height=250).project(
type='mercator', reflectY=False, scale=170, translate=[400, 50])





aus_asia_chart = alt.Chart(data_url_geojson,title='Australia, New Zealand and East Asia').mark_geoshape(stroke='white').transform_filter(alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Asia', 'Oceania', ])).transform_filter(alt.FieldOneOfPredicate(field='properties.region_wb', oneOf=['East Asia & Pacific', ])
    ).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating",'rating_bins', 'rating_bins_num']),
    ).transform_filter(
    'isValid(datum.rating_bins_num)'
).encode(
        fill=alt.Color(
            "rating_bins_num:O",
          
            legend=alt.Legend(title='Average PISA Scores', labelExpr=axis_labels),
            scale=alt.Scale(scheme="reds", reverse=True),
        ), 
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).properties(width=400, height=250).project(type='equalEarth',  scale=120, translate=[200, 90], rotate=[-135, -25 ,0])


aus_asia_base = alt.Chart(data_url_geojson).mark_geoshape(    fill='#666666',
    stroke='white').encode(tooltip=[alt.Tooltip("properties.name:N", title="Country")]).transform_filter(alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Asia', 'Oceania', ])).transform_filter(alt.FieldOneOfPredicate(field='properties.region_wb', oneOf=['East Asia & Pacific', ])).properties(width=400, height=250).project(type='equalEarth',  scale=120, translate=[200, 90], rotate=[-135, -25 ,0])

final_chart = alt.hconcat(
    alt.vconcat(na_base + na_chart, sa_base + sa_chart),
    alt.vconcat(eu_base + eu_chart, aus_asia_base+aus_asia_chart)

)
st.altair_chart(final_chart, use_container_width=True)

st.caption("Data taken from OECD's PISA scores from 2003-2018. The very low scores are below 474.6, low is between 474.6 and 491.2, medium is between 491.2 and 501.8, high ranges between 501.8, 516 and very high is any score above 516. ")

st.write("OECD reports that part of the function of PISA is to allow benchmarking of a country's performance and to see what instructional methods are effective. This can be seen with Finland’s consistently high scores and the best-selling book “Teach Like Finland.” OECD touts the success of Germany in using the data to change the school structure and increase scores. However, while as impressive as it sounds, this is not the whole picture. Improvement did occur, but the long-term scoring showed a decrease in student scores for Germany. However, Germany is not alone. The overall average score for PISA has gone down.")

st.subheader("Visualization 2: Improvement and Deterioration of PISA Scores Over Time")

sex_choices=list(pisa_df["sex"].unique())
sex_choices.sort(reverse=True)


selected_sex = st.radio('Select Sex (Or Total of Both):', options=sex_choices, index=0)
pisa_sex_filtered = pisa_df[pisa_df['sex'] == selected_sex]


pisa_sex_df = pisa_sex_filtered.groupby(['country_name', 'time'])['rating'].mean().reset_index()
# get the scores of the 2018 rating - 2003 rating
pisa_sex_df = pisa_sex_df.pivot(index='country_name', columns='time', values='rating')
pisa_sex_df['change'] = pisa_sex_df[2018] - pisa_sex_df[2003]
pisa_sex_df = pisa_sex_df.sort_values(by='change', ascending=False)
pisa_sex_df['change2'] = pisa_sex_df[2018] - pisa_sex_df[2006]
# if change is null, merge change 2
pisa_sex_df['change'] = pisa_sex_df['change'].fillna(pisa_sex_df['change2'])
# make all column headers into strings
pisa_sex_df.columns = pisa_sex_df.columns.astype(str)
pisa_sex_df = pisa_sex_df.reset_index()
# drop na in change column
pisa_sex_df = pisa_sex_df.dropna(subset=['change'])

# change United States to USA, United Kingdom to UK, Netherlands (kingdom of the) to Netherlands, Korea to South Korea, 'Türkiye' to Turkey
pisa_sex_df.loc[pisa_sex_df['country_name'] == 'United States of America', 'country_name'] = 'USA'
# 'United Kingdom of Great Britain and Northern Ireland'
pisa_sex_df.loc[pisa_sex_df['country_name'] == 'United Kingdom of Great Britain and Northern Ireland', 'country_name'] = 'UK'
pisa_sex_df.loc[pisa_sex_df['country_name'] == 'Netherlands (Kingdom of the)', 'country_name'] = 'Netherlands'
# 'Republic of Korea'
pisa_sex_df.loc[pisa_sex_df['country_name'] == 'Republic of Korea', 'country_name'] = 'South Korea'
# 'Türkiye'
pisa_sex_df.loc[pisa_sex_df['country_name'] == 'Türkiye', 'country_name'] = 'Turkey'



# change in ratings plot 
change_rating_chart = alt.Chart(pisa_sex_df).mark_bar(color='royalblue').encode(
    y=alt.Y('change:Q', title='Change in Average PISA Score'),
    # move x axis labels down from the line

    x=alt.X('country_name:N', title='Country', axis=alt.Axis(labelFontSize=10.5, labelPadding=10), sort='-y'),
    # color='blue',
    tooltip=['change', 'country_name'], 
    # sort least to greatest
    order=alt.Order('change:Q', sort='descending'),
).properties(
    title='Change in Average PISA Score from 2003 to 2018',
    width=800

)

st.altair_chart(change_rating_chart, use_container_width=False)

st.caption("Most developing countries and those in the Eastern European Block have seen their scores increase over time. A caveat for this visualization is that some countries did not participate in PISA in 2003. For Estonia, Israel, the UK, Slovenia, and Chile, the change in scores is from 2006 - 2018.")


st.write("While a country’s overall performance remains consistent, the order does change as sex selection changes. Girls often show a more robust performance on the assessments than their male classmates. Some explanations have been offered, including the format of the test. The goal of PISA is to test work-readiness skills. To do this, the assessment gives reading passages and then has students answer questions based on the reading. These readings change based on the subject of the test, math, reading, or science. You can take a [practice math assessment]('https://www.khanacademy.org/test-prep/oecd-pisa/x24097bf202654aa9:welcome-to-pisa/x24097bf202654aa9:welcome/a/test-prep-welcome-to-pisa') through Khan Academy. The exam format has come under fire, as the translations of readings from English to other languages can begin to give away even more context and cause differences in its efficacy.")


st.write("When conducting PISA, students are also prompted to complete a questionnaire providing background information, including their interest in pursuing a career in topics such as science or seeing themselves as scientists. These findings often correlate negatively with score performance. This means students who score well in science do not see themselves as scientists. This can cause concern as students may show promise in scientific fields but lack the confidence to see themselves within a field. This is often more common for girls in male-dominated fields, as well as students of color, thus continuing a lack of diversity and perspective in many fields. The questionnaire also details schools Information Computer & Technology (ICT) usage. These questions are geared towards determining small details like the internet connectivity at the school to larger scale things like if each student has access to a tablet or laptop and how often they are employed in lessons. Finland, consistently ranked as the top-performing country, reports the lowest amount of ICT usage. Meanwhile, its Nordic neighbor, Norway, reports the highest usage out of OECD countries and has average scores.")

st.write("The questionnaire also reveals interesting cultural norms. Since PISA is considered “low-stakes,” the scores are never reported back to the students, teachers, or schools; they are only revealed nationally, and the effort a student may put in could differ. On a scale of 1-10, students are asked two questions regarding how much effort they put into the PISA and how much effort they put into an examination. Swedish students had the most significant difference in the answers, while students from Japan and Korea gave higher scores for both questions.")

st.write("These questions raise a question: PISA is often used to justify a bigger or smaller budget for education in a country, justifying moving above an average. However, is the budget for education really what moves the needle? The discourse around US standardized testing constantly tells us that a student's socioeconomic status is a strong predictor of academic success and performance.")

st.subheader("What correlates with PISA scores?")

st.subheader("Visualization 3: Comparing Gini Index and Education Expenditure (as % GDP) to PISA Scores")



# scatter plot where rating is y and gini index is x, color is the country use altair
country_codes_all = pd.read_csv(
    "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
)

pisa_total = pisa_total.merge(country_codes_all, left_on='code', right_on='alpha-3')
pisa_total.drop(columns=['alpha-2', 'alpha-3', 'country-code', 'iso_3166-2', 'region-code', 'sub-region-code', 'intermediate-region-code',  'intermediate-region', 'iso_3166-2'], inplace=True)

pisa_total['new_region'] = pisa_total['region'].replace({'Europe': 'Europe', 'Asia': 'Asia and Oceania', 'Africa': 'Africa', 'Americas': 'North and South America', 'Oceania': 'Asia and Oceania'})

# japan 2013 - 32.9 https://data.worldbank.org/indicator/SI.POV.GINI
# south korea 2016 - 31.4 https://data.worldbank.org/indicator/SI.POV.GINI
# iceland 2017 - 26.1 https://data.worldbank.org/indicator/SI.POV.GINI
# chile 2017 - 45.3 https://data.worldbank.org/indicator/SI.POV.GINI?locations=CL
# put those values in for the missing values in 2018
pisa_total.loc[(pisa_total['country_name'] == 'Japan')& (pisa_total['time'] == 2018), 'gini_index'] = 32.9
pisa_total.loc[(pisa_total['country_name'] == 'Republic of Korea') & (pisa_total['time'] == 2018), 'gini_index'] = 31.4
pisa_total.loc[(pisa_total['country_name'] == 'Iceland')& (pisa_total['time'] == 2018), 'gini_index'] = 26.1
pisa_total.loc[(pisa_total['country_name'] == 'Chile') & (pisa_total['time'] == 2018), 'gini_index'] = 45.3

pisa_total_2018 = pisa_total[pisa_total['time'] == 2018]

domain = ['Asia and Oceania', "Europe", "North and South America"]
range_ = ['darkgreen', 'mediumvioletred', 'dodgerblue']
chart_gini = alt.Chart(pisa_total_2018).mark_circle(size=40).encode(
    x = alt.X('gini_index:Q', scale=alt.Scale(domain=(20, 60)), title='Gini Index', axis=alt.Axis(grid=False)),
    y = alt.Y('rating:Q', scale=alt.Scale(domain=(360, 560)), title='Average PISA Scores'),    
    color=alt.Color('new_region:N', scale=alt.Scale(domain=domain, range=range_), legend=alt.Legend(title='Region')),

    tooltip = [alt.Tooltip('country_name:N', title='Country'), alt.Tooltip('rating:Q', title='Average PISA Score'), alt.Tooltip('gini_index:Q', title='Gini Index')]
).properties(
    width=350,
    height=400
).interactive()
trend_gini = chart_gini.transform_regression('gini_index', 'rating').mark_line(color = 'dimgrey', strokeWidth=1.4).encode(color = 
     alt.Color(legend=None))


domain = ['Asia and Oceania', "Europe", "North and South America"]
range_ = ['darkgreen', 'mediumvioletred', 'dodgerblue']
chart_education = alt.Chart(pisa_total_2018).mark_circle(size=40).encode(
 
    x = alt.X('expenditure_on _education_pct_gdp:Q', scale=alt.Scale(domain=(2, 8)), title='Education Expenditure as Percent GDP', axis=alt.Axis(tickCount=12, grid=False)),
    y = alt.Y('rating:Q', scale=alt.Scale(domain=(340, 560)), title='Average PISA Scores'), 

    color = alt.Color('new_region:N', scale=alt.Scale(domain=domain, range=range_), legend=alt.Legend(title='Region')),
  
    tooltip = [alt.Tooltip('country_name:N', title='Country'), alt.Tooltip('rating:Q', title='Average PISA Score'), alt.Tooltip('expenditure_on _education_pct_gdp:Q', title='Education Expenditure (%)', format='.2f')]
).properties(
    width=350,
    height=400
).interactive()
trend_education = chart_education.transform_regression('expenditure_on _education_pct_gdp', 'rating').mark_line(color = 'dimgrey', strokeWidth=1.4).encode(color = alt.Color(legend=None))

# show gini and education plots next to each other
final_scatter = alt.hconcat((chart_gini + trend_gini), (chart_education + trend_education)).resolve_scale(y="shared").interactive()

st.altair_chart(final_scatter, use_container_width=True)


st.caption("While government expenditure on education is not a strong indicator of PISA scores, the country's Gini index does provide context for the PISA score.")


st.write("The Gini index measures equality, with scores close to zero indicating an equal society and higher scores indicating various inequality measures. The Gini index looks at income and how an individual or household compares to a normal distribution, suggesting that countries with more social safety nets tend to have higher PISA scores than countries with minimal social safety nets. While education spending can contribute to greater socioeconomic security, this is often made up of subsidies for families with children, pricing, availability of food, and healthcare expenses. It's interesting to note that higher education funding relative to a country's GDP has absolutely no correlation with better PISA performance. Education funding varies by country, with different levels of government responsible for various education levels. For example, the US ranks high in terms of student spending on average. However, the US funding system based on property taxes is not evenly distributed, with some students getting much more funding than others based on their zip code.")

st.write("The PISA test is not particularly insightful for the US, which leaves education as a state's right. However, when grouping US states by levels of child poverty, the states perform similarly to countries with similar childhood poverty levels. While PISA scores may be telling of student understanding at the moment, improving the score may be more about supporting children and their families with accessing basic needs than pushing education funding. This is not unique to the US. Vietnam, which has started to take the test, only has 56% of its 15-year-olds in school. The test does not reflect that much of the population leaves the schooling system by the time PISA would be administered. We see other instances where the test results do not accurately reflect the population. The scores that have no impact on students bear more weight with a nation's minister of education, who will need to explain the country's poor performance or celebrate its stellar performance to government officials and the world at large. While standardized tests can offer insight into a country's progress in its education system, they do not point to where or why these successes or failures are happening.")


st.subheader('References:')
st.write('Association, N. E. (2020, June 25). History of standardized testing in the United States. NEA. https://www.nea.org/professional-excellence/student-engagement/tools-tips/history-standardized-testing-united-states')
st.write('Every student succeeds act (ESSA). Every Student Succeeds Act (ESSA) | U.S. Department of Education. (n.d.). https://www.ed.gov/essa')
st.write('Gershon, L. (2015, May 12). A short history of standardized tests - JSTOR DAILY. JSTOR Daily. https://daily.jstor.org/short-history-standardized-tests/')
st.write('Lehigh University College of Education. (2013, October 18). History of standardized testing. History of Standardized Testing. https://ed.lehigh.edu/news-events/news/history-standardized-testing')
st.write('OECD. (n.d.). Pisa - Pisa. Programme for International Student Assessment. https://www.oecd.org/pisa/')
st.write('Posner, D. (2004). What’s wrong with teaching to the test? Phi Delta Kappan, 85(10), 749–751. https://doi.org/10.1177/003172170408501009')
st.write('Robin Harwick, Ph. D. (2020, October 5). Teaching to the test harms students. Medium. https://medium.com/the-faculty/teaching-to-the-test-harms-students-5f9752e0c9bf')

st.write('Sjøberg, S., & Jenkins, E. (2020). Pisa: A political project and a research agenda. Studies in Science Education, 58(1), 1–14. https://doi.org/10.1080/03057267.2020.1824473 ')

