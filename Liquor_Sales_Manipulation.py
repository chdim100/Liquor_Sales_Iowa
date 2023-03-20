import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


###### import Liquor_Sales_2016_2019.csv which includes Liquor Sales 
###### in the state of Iowa in USA between 2016-2019. 
file2read='Liquor_Sales_2016_2019.csv'
df=pd.read_csv(file2read)
Nc=4

#########----first inspection-----
###### get columns' names:
print(df.columns,'\n')
##### select to display Nc columns
pd.set_option('display.max_columns', Nc)
###### check headers (first 10 rows)'
print(df.head(10))

###### show most popular (top sales) item IDs in Iowa
print(df['item_number'].value_counts())

####### group by zip code and item number, sum of bottles 
####### sold per item in each zip code
bottles_items_by_zip=df.groupby(['zip_code','item_number','item_description'])\
    ['bottles_sold'].sum()
#### to numpy
zipcodes=np.array(bottles_items_by_zip.index.get_level_values(0),dtype=np.intc)
itemids=np.array(bottles_items_by_zip.index.get_level_values(1),dtype=np.intc)
itemdesc=np.array(bottles_items_by_zip.index.get_level_values(2))
bottles1=bottles_items_by_zip.to_numpy(dtype=np.intc)
data1=np.array([zipcodes,itemids,itemdesc,bottles1])

####### visualize with Seaborn scatterplot
axes1=sns.scatterplot(x=zipcodes,y=bottles1,hue=itemdesc,\
                  data=itemids)
axes1.set(xlabel='Zip Code', ylabel='# of bottles sold')
plt.title('Bottles sold by zip code and item')

plt.legend(ncol=4,shadow=True,bbox_to_anchor=(0.5, -0.55), \
           loc='lower center', borderaxespad=0)
plt.setp(axes1.get_legend().get_texts(), fontsize='7')
plt.subplots_adjust(bottom=0.35)
plt.xlim(min(zipcodes),max(zipcodes))
plt.ylim(-10,max(bottles1)+100)
major_ticks = np.arange(min(zipcodes), max(zipcodes), 250)
minor_ticks = np.arange(min(zipcodes), max(zipcodes), 50)
axes1.set_xticks(major_ticks)
axes1.set_xticks(minor_ticks, minor=True)
axes1.grid(which='minor', alpha=0.2)
axes1.grid(which='major', alpha=0.5)
manager = plt.get_current_fig_manager()
manager.window.showMaximized()

##### function visualize with Seaborn horizontal barplot
def create_horz_barplot(df,TopN,palette,saleskey):
    storeids=np.array(df.index.get_level_values(0),dtype=np.intc)
    store_city=np.array(df.index.get_level_values(1))
    storeinfo=np.column_stack((storeids,store_city))
    storeinfoall=np.apply_along_axis(lambda d: str(d[0]) + ', ' +\
                                     d[1], 1, storeinfo)
    percvals=df.to_numpy()
    plt.figure()
    axes=sns.barplot(y=storeinfoall[0:TopN],x=percvals[0:TopN],palette=palette)
    axes.set(xlabel='Sales Percentage (%)', ylabel='Store, City')
    plt.title('Top '+str(TopN)+' Stores by sales '+saleskey+' percentage')
    axes.grid()
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()


######################################################
####### group by store (number), sum of sales (in bottles) per store
TopN=20
saleskey='(bottles)'
bottles_by_store=df.groupby(['store_number','city'])['bottles_sold'].sum()
TotalSalesBottles=np.sum(bottles_by_store)
percofbottles_by_store=100*bottles_by_store/TotalSalesBottles
percofbottles_by_store_sort=percofbottles_by_store.sort_values\
    (ascending=False).round(decimals=2)
palette='GnBu_d'
create_horz_barplot(percofbottles_by_store_sort,TopN,palette,saleskey)


####### group by store (number), sum of sales ($) per store
TopN=20
saleskey='($)'
sales_by_store=df.groupby(['store_number','city'])['sale_dollars'].sum()
TotalSales=np.sum(sales_by_store)
##### get percentages
percofsales_by_store=100*sales_by_store/TotalSales
percofsales_by_store_sort=percofsales_by_store.sort_values\
    (ascending=False).round(decimals=2)
palette='YlOrBr'
create_horz_barplot(percofsales_by_store_sort,TopN,palette,saleskey)

####### group by store (number), sum of sold gallons per store
TopN=20
saleskey='(gallons)'
gallons_by_store=df.groupby(['store_number','city'])\
    ['volume_sold_gallons'].sum()
TotalGallons=np.sum(gallons_by_store)
##### get percentages
percofgallons_by_store=100*gallons_by_store/TotalGallons
percofgallons_by_store_sort=percofgallons_by_store.sort_values\
    (ascending=False).round(decimals=2)
palette='icefire'
create_horz_barplot(percofgallons_by_store_sort,TopN,palette,saleskey)