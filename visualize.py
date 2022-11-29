
import pandas
import seaborn
import matplotlib.pyplot as plt


def transform_data(data: pandas.DataFrame, columns: list[str], timestep: str, value_name: str, var_name: str) -> pandas.DataFrame:
        data = data.filter(items=columns).dropna()
        data[timestep] = data.index 
        data = data.melt(id_vars=[timestep], value_vars=columns, value_name=value_name, var_name=var_name)
        return data


def run():
    all_data = pandas.read_csv('output.csv')
    seaborn.set_theme(style='white', context='talk')
    plt.rcParams["figure.figsize"] = (8.3, 8.3)
    plt.rcParams['font.size'] = '16'
    plt.rcParams['legend.fontsize'] = '14'

    #Average Hourly Customers Plot
    data = transform_data(all_data, ['Average Hourly Customers'], 'Hours', 'Customers', '')    
    avg_customers = seaborn.barplot(data, x='Hours', y='Customers', palette='Blues', hue='Customers', dodge=False).legend([], [], frameon=False).figure
    
    #Daily customers vs Walkout customers 
    data = transform_data(all_data, columns=['Total Daily Customers', 'Daily Walkout Customers'], timestep='Days', value_name='Customers', var_name='Interaction Type')
    daily_customers = seaborn.relplot(data, x='Days', y='Customers', hue='Interaction Type', kind='line', palette='muted').figure

    #Market product prices 
    data = transform_data(all_data, columns=['Market Milk Price', 'Market Coffee Price', 'Market Sugar Price'], timestep='Days', value_name='Price', var_name='Product')
    market_prices = seaborn.relplot(data, x='Days', y='Price', hue='Product', kind='line', palette='muted').figure


    # Cost breakdown
    data = all_data.filter(items=
                ['Daily Milk Cost', 'Daily Coffee Cost', 'Daily Sugar Cost', 'Daily Employee Cost']
            ).dropna()
    data = pandas.DataFrame(index=['Milk', 'Coffee', 'Sugar', 'Employee'], data={
        'Price': [data['Daily Milk Cost'].mean(), data['Daily Coffee Cost'].mean(), 
                  data['Daily Sugar Cost'].mean(), data['Daily Employee Cost'].mean()]
    }).sort_values('Price', ascending=False)
    seaborn.set_palette('muted')
    costs = data.plot(kind='pie', y='Price', autopct='%.2f%%', labels=None, ylabel='').figure


    #Gross income, gross expense, net income 
    data = transform_data(all_data, columns=['Gross Daily Income', 'Gross Daily Expense', 'Net Daily Income'], timestep='Days', value_name='Money', var_name='Category')
    income = seaborn.relplot(data, x='Days', y='Money', hue='Category', kind='line', palette='muted').set(ylim=(0, 1500)).figure

    seaborn.despine()

    avg_customers.savefig('images/hourly_customers.png', format='png')
    daily_customers.savefig('images/daily_customers.png', format='png')
    market_prices.savefig('images/market_prices.png', format='png')
    costs.savefig('images/costs.png', format='png')
    income.savefig('images/income.png', format='png')


