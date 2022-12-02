
import pandas
import seaborn
import matplotlib.pyplot as plt


'''
    A good portion of the code here is just reformatting the data so that Seaborn & Matplotlib are happy with it. 
    To change the appearence of the graphs, focus on the lines of the form:
        `variable = seaborn.plot(data, ...).figure`
    Some figures, like the pie chart, use `data.plot` instead, but the idea is the same. 
    By changing the options of the function, or adding additional options, the appearnce will change. 
    Check the Seaborn and Matplotlib documentation for a rundown of the different options.
'''


# Helper function to melt the data to a format Seaborn likes better (https://seaborn.pydata.org/tutorial/data_structure.html#long-form-vs-wide-form-data)
def transform_data(data: pandas.DataFrame, columns: list[str], timestep: str, value_name: str, var_name: str) -> pandas.DataFrame:
        data = data.filter(items=columns).dropna()
        data[timestep] = data.index 
        data = data.melt(id_vars=[timestep], value_vars=columns, value_name=value_name, var_name=var_name)
        return data



def run():
    all_sim_data = pandas.read_csv('output.csv')
    optimize_data = pandas.read_csv('optimize.csv')
    model_test_data = pandas.read_csv('test_model.csv')

    seaborn.set_theme(style='white', context='talk')
    plt.rcParams["figure.figsize"] = (8.3, 8.3)
    plt.rcParams['font.size'] = '16'
    plt.rcParams['legend.fontsize'] = '14'

    #Average Hourly Customers Plot
    data = transform_data(all_sim_data, ['Average Hourly Customers'], 'Hours', 'Customers', '')    
    avg_customers = seaborn.barplot(data, x='Hours', y='Customers', palette='Blues', hue='Customers', dodge=False).legend([], [], frameon=False).figure
    
    #Daily customers vs Walkout customers 
    data = transform_data(all_sim_data, columns=['Total Daily Customers', 'Daily Walkout Customers'], timestep='Days', value_name='Customers', var_name='Interaction Type')
    daily_customers = seaborn.relplot(data, x='Days', y='Customers', hue='Interaction Type', kind='line', palette='muted').set(ylim=0).figure

    #Market product prices 
    data = transform_data(all_sim_data, columns=['Market Milk Price', 'Market Coffee Price', 'Market Sugar Price'], timestep='Days', value_name='Price', var_name='Product')
    market_prices = seaborn.relplot(data, x='Days', y='Price', hue='Product', kind='line', palette='muted').figure


    # Cost breakdown
    data = all_sim_data.filter(items=
                ['Daily Milk Cost', 'Daily Coffee Cost', 'Daily Sugar Cost', 'Daily Employee Cost']
            ).dropna()
    data = pandas.DataFrame(index=['Milk', 'Coffee', 'Sugar', 'Employee'], data={
        'Price': [data['Daily Milk Cost'].mean(), data['Daily Coffee Cost'].mean(), 
                  data['Daily Sugar Cost'].mean(), data['Daily Employee Cost'].mean()]
    }).sort_values('Price', ascending=False)
    seaborn.set_palette('muted')
    costs = data.plot(kind='pie', y='Price', autopct='%.2f%%', labels=None, ylabel='').figure


    #Gross income, gross expense, net income 
    data = transform_data(all_sim_data, columns=['Gross Daily Income', 'Gross Daily Expense', 'Net Daily Income'], timestep='Days', value_name='Money', var_name='Category')
    income = seaborn.relplot(data, x='Days', y='Money', hue='Category', kind='line', palette='muted').set(ylim=0).figure

    #Optimizations 
    data = optimize_data.filter(items=['Daily Customers', 'Price per Ounce', 'Number of Employees']).dropna()
    data = data.melt(id_vars=['Daily Customers'], value_vars=['Price per Ounce', 'Number of Employees'], value_name='Count', var_name='Type')
    optimizations = seaborn.relplot(data, x='Daily Customers', y='Count', hue='Type', kind='line', palette='muted').figure


    #Model test 
    data = model_test_data.filter(items=['Functional Revenue', 'Agent Revenue', 'Drink Price']).dropna()
    data = data.melt(id_vars=['Drink Price'], value_vars=['Functional Revenue', 'Agent Revenue'], value_name='Revenue', var_name='Model Type')
    model_test = seaborn.relplot(data, x='Drink Price', y='Revenue', hue='Model Type', kind='line', palette='muted').figure

    seaborn.despine()


    # Save all figures
    avg_customers.savefig('images/hourly_customers.png', format='png')
    daily_customers.savefig('images/daily_customers.png', format='png')
    market_prices.savefig('images/market_prices.png', format='png')
    costs.savefig('images/costs.png', format='png')
    income.savefig('images/income.png', format='png')
    optimizations.savefig('images/optimizations.png', format='png')
    model_test.savefig('images/model_test.png', format='png')


run()


