import datetime
from colorama import Fore, Back, Style
from utilities import key_press, clear_screen

"""
This file contains the classes, function and variables for
the user processes for configuring the report calculations.
The file is meant to be imported into and called from a parent file
for deployment.
"""


class InvalidPercents(Exception):
    """
    Raise when percents don't add up to 100
    """
    pass


class InvalidDateRange(Exception):
    """
    Raise when years are out of range
    """
    pass


class InvalidRegion(Exception):
    """
    Raise when region(s) entered are not in list
    """
    pass


def years_min_max(stat_dict):
    """
    Returns the earliest and lastest statistic years in the dictionary
    """
    years_loaded = set()
    for country in stat_dict:
        for country_stats in country['statistic']:
            years_loaded.add(country_stats['year'])
    years_loaded.remove(None)
    first_year = min(years_loaded)
    last_year = max(years_loaded)
    return ([first_year, last_year])


def input_years(stats_dict):
    """
    Prompts user for date range report configuration
    """
    range_of_years = years_min_max(stats_dict)
    print(Fore.WHITE + ' \n')
    print(f'Now set the range of years for your report')
    print(f'\nPlease enter a start year and an end year between '
          f'{range_of_years[0]} to: {range_of_years[1]} (inclusive)')
    years_unset = True
    while years_unset:
        try:
            start_year = input('Report start year:\n')
            end_year = input('Report end year:\n')
            if not (start_year >= range_of_years[0] and
               end_year <= range_of_years[1] and
               start_year > end_year):
                raise InvalidDateRange
            else:
                return ([start_year, end_year])
        except InvalidDateRange:
            print(Fore.RED + f'\nYears must be between {range_of_years[0]} and '
                  f'{range_of_years[1]}, please try again')
            print(Style.RESET_ALL)


def regions_loaded(stats_dict):
    """
    Returns a list of regions
    Assumes all other report options have same years loaded
    """
    regions_loaded = set()
    for country in stats_dict:
        regions_loaded.add(country['region_code'])
    regions_loaded.remove(None)
    regions_sorted = list(regions_loaded)
    regions_sorted.sort()
    return (regions_sorted)


def input_regions(stats_dict):
    """
    Prompts user to select region(s) for report configuration
    """
    region_list = regions_loaded(stats_dict)
    print(Style.RESET_ALL)
    print(f'Now choose the region or regions to report on.\n')
    print(f'Please enter one or more of the following region codes.')
    print(f'If you would like to report on more than one region, then '
          f'please separate them with commas, without spaces,'
          f' similarly to the list below.')
    display_list = ','.join([str(elem) for elem in region_list])
    print(display_list)
    regions_unset = True
    while regions_unset:
        try:
            input_regions = (input('Report region(s):\n')).upper()
            input_regions = input_regions.rsplit(',')
            report_regions = list(set(input_regions) & set(region_list))
            if (len(report_regions) == len(input_regions)):
                return (report_regions)
            else:
                raise InvalidRegion
        except InvalidRegion:
            print(Fore.RED + f'\nRegions must be from the list and in '
                  f'the same format,\n'
                  f'Valid region codes are: \n {display_list}\n'
                  f'You entered: \n {input_regions}\n'
                  f'please try again')
                print(Style.RESET_ALL)
            continue
    return (report_regions)


def input_weights():
    """
    Prompts user for study weight report configuration
    """
    print(Fore.RED + f'This feature will be in next release\n')
    print(Fore.BLUE + f'There are 3 report studies '
          f'available for your report:\n'
          f'\t Disposable Income, Population, Urbanisation\n')
    print(f'Please enter 3 values 1 for each study\n'
          f'each value represents the percent out of 100% \n'
          f'to be applied to the study values')
    pct_unset = True
    while pct_unset:
        try:
            print(Fore.BLUE + '')
            disp_pct = int(input('Disposable Income %:\n'))
            popu_pct = int(input('Population %:\n'))
            urba_pct = int(input('Urbanisation %:\n'))
            if ((disp_pct + popu_pct + urba_pct) != 100):
                raise InvalidPercents
            else:
                return ([disp_pct, popu_pct, urba_pct])
        except InvalidPercents:
            print(Fore.RED + f'\nAmounts entered do not sum to 100,'
                  f' please try again')
        except ValueError:
            print(Fore.RED + f'\nNumbers only, please try again')


def input_rpt_options(weights, years, regions, stats_dict):
    """
    Collect report options from user
    option functions return a list of values
    """
    print('Next step is to configure your report\n')
    weights = input_weights()
    years = input_years(stats_dict)
    regions = input_regions(stats_dict)
    return ([weights, years, regions])
