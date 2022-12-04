
import pandas
import seaborn
import matplotlib.pyplot as plt


'''
    A good portion of the code here is just reformatting the data so that Seaborn & Matplotlib are happy with it. 
    To change the appearence of the graphs, focus on the lines of the form:
        `variable = seaborn.plot(data, ...)`
    Some figures, like the pie chart, use `data.plot` instead, but the idea is the same. 
    By changing the options of the function, or adding additional options, the appearnce will change. 
    Check the Seaborn and Matplotlib documentation for a rundown of the different options.
'''


# Helper function to filter out columns
def transform_data(data: pandas.DataFrame, columns: list[str], timestep: str) -> pandas.DataFrame:
    data = data.filter(items=columns).dropna()
    data[timestep] = data.index 
    return data



def run():
    all_sim_data = pandas.read_csv('output.csv')
    optimize_data = pandas.read_csv('optimize.csv')
    model_test_data = pandas.read_csv('test_model.csv')

    plt.rcParams['figure.figsize'] = 8, 11
    plt.rcParams['font.size'] = 12

    seaborn.despine()

    #Average Hourly Customers Plot
    hourly_data = transform_data(all_sim_data, ['Average Hourly Customers'], timestep='Hours')
    daily_data = transform_data(all_sim_data, columns=['Total Daily Customers', 'Daily Walkout Customers'], timestep='Days')

    fig, [hourly_customers_plot, customer_info_plot] = plt.subplots(2)
    customer_info_plot.set_title("Successful Customers vs. Walkout Customers")
    customer_info_plot.set_xlabel('Days')
    customer_info_plot.set_ylabel('Customers')
    hourly_customers_plot.set_xlabel('Hours')
    hourly_customers_plot.set_ylabel('Customers')
    hourly_customers_plot.set_title("Average Hourly Customers")

    hourly_customers_plot.bar(hourly_data['Hours'], hourly_data['Average Hourly Customers'])
    customer_info_plot.plot(daily_data['Days'], daily_data['Total Daily Customers'], label='Sucessful Customers')
    customer_info_plot.plot(daily_data['Days'], daily_data['Daily Walkout Customers'], label='Walkout Customers')
    plt.legend(bbox_to_anchor=(0.5, -0.3), loc='lower center')
    plt.savefig('images/customer_info.png', dpi=130, bbox_inches='tight', pad_inches=0.4)
    plt.clf()

    #Market product prices, cost breakdown, income/expenses
    market_data = transform_data(all_sim_data, ['Market Milk Price', 'Market Coffee Price', 'Market Sugar Price'], timestep='Days')
    cost_breakdown = [
        all_sim_data['Daily Milk Cost'].mean(), all_sim_data['Daily Coffee Cost'].mean(), 
        all_sim_data['Daily Sugar Cost'].mean(), all_sim_data['Daily Employee Cost'].mean()
    ]
    income_data = transform_data(all_sim_data, columns=['Gross Daily Income', 'Net Daily Income', 'Gross Daily Expense'], timestep='Days')

    market_data_plot = plt.subplot(2, 2, 1)
    cost_breakdown_plot = plt.subplot(2, 2, 2)
    income_data_plot = plt.subplot(2, 1, 2)

    market_data_plot.set_title("Market Goods Price")
    market_data_plot.set_ylabel('Price')
    market_data_plot.set_xlabel('Days')

    income_data_plot.set_title('Income and Expenses')
    income_data_plot.set_ylabel('Money')
    income_data_plot.set_xlabel('Days')

    cost_breakdown_plot.set_title('Cost Breakdown')

    for col in market_data.loc[:, market_data.columns != 'Days']: market_data_plot.plot(market_data['Days'], market_data[col])
    cost_breakdown_plot.pie(cost_breakdown, autopct='%.2f%%', radius=1.2)
    for col in income_data.loc[:, income_data.columns != 'Days']: income_data_plot.plot(income_data['Days'], income_data[col], label=col)
    
    market_data_plot.legend(['Milk', 'Coffee', 'Sugar'], bbox_to_anchor=(-0.55, 0.5), loc='center')
    income_data_plot.legend(['Gross Income', 'Net Income', 'Gross Expense'], bbox_to_anchor=(-0.3, 0.5), loc='center')
    cost_breakdown_plot.legend(['Milk', 'Coffee', 'Sugar', 'Employees'], loc='center', bbox_to_anchor=(1.3, 0.8))
    plt.savefig('images/financial_info.png', format='png', bbox_inches='tight', pad_inches=0.4)
    plt.clf()

    #Optimizations 
    data = optimize_data.filter(items=['Daily Customers', 'Price per Ounce', 'Number of Employees']).dropna()
    data = data.melt(id_vars=['Daily Customers'], value_vars=['Price per Ounce', 'Number of Employees'], value_name='Count', var_name='Type')
    optimizations = seaborn.relplot(data, x='Daily Customers', y='Count', hue='Type', kind='line', palette='muted')


    #Model test 
    data = model_test_data.filter(items=['Functional Revenue', 'Agent Revenue', 'Drink Price']).dropna()
    data = data.melt(id_vars=['Drink Price'], value_vars=['Functional Revenue', 'Agent Revenue'], value_name='Revenue', var_name='Model Type')
    model_test = seaborn.relplot(data, x='Drink Price', y='Revenue', hue='Model Type', kind='line', palette='muted')


    # Save all figures
    optimizations.figure.savefig('images/optimizations.png', format='png')
    model_test.figure.savefig('images/model_test.png', format='png')


