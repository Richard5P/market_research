"""
This file contains the classes, function and variables for
calculating the analytical report based on the configured statistics.
The file is meant to be imported into and called from a parent file for
deployment.
"""


def calc_stat_sum(reg_stat_data):
    """
    Sum values for each region, stat_type
    """
    stats_sum = {}
    for line in reg_stat_data:
        if line[0] in stats_sum.keys():
            if line[1] in stats_sum[line[0]].keys():
                stats_sum[line[0]][line[1]] += line[2]
            else:
                stats_sum[line[0]][line[1]] = line[2]
        else:
            stats_sum[line[0]] = {line[1]: line[2]}
    return (stats_sum)


def calc_reg_stat_data(years, regions, stats_dict):
    """
    Using the report options, calculate the average statistic values
    for each region and type of statistic across the range of years.
    The calculations will support regional reporting and future
    country reporting.
        country_avg =
            sum_value (for range of years)/number of years
        region_avg =
            sum country_avg (for countries in region)/
                number of countries in region
    Return a list of lists: [region code, stat code, avg value]
    Assumes the stats_dict is sorted by country by region
    """
    num_years = float(int(years[1]) - int(years[0]))
    reg_stat_data = [
        {'region_code': None, 'stat_code': None, 'value_sum': None}]
    for country in stats_dict:
        sum_value = 0.0
        if country['region_code'] in regions:
            sum_region = country['region_code']
            for statistic in country['statistic']:
                sum_stat_code = statistic['stats_code']
                if statistic['year'] >= years[0] and \
                   statistic['year'] <= years[1]:
                    sum_value = sum_value + float(statistic['value'])
                country_avg = sum_value / num_years
            reg_stat_data.append([{'region_code': sum_region,
                                   'stat_code': sum_stat_code, 
                                   'value_sum': country_avg}])
    return (reg_stat_data)


def calc_report_values(weights, reg_sta_sum):
    """
    Weights statistics for reporting
    """
    return (reg_sta_sum)


def calc_report_data(weights, years, regions, stats_dict):
    """
    Calls functions to:
        1. Calculate country value averages for date range
           and sum it by stat_type and region
        2. Sum the stat_type and region values
        3. Weight the summed values for reporting hierarchy
    returns the report ready list
    """
    reg_stat_data = calc_reg_stat_data(years, regions, stats_dict)
    reg_stat_sum = calc_stat_sum(reg_stat_data)
    selection_results = calc_report_values(weights, reg_stat_sum)
    return (selection_results)


def calc_stats(report_options, stats_dict):
    """
    """
    weights = report_options[0]
    years = report_options[1]
    regions = report_options[2]
    selection_results = calc_report_data(weights, years, regions, stats_dict)
    return (selection_results)
