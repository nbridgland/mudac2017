#created to search for diag codes we don't want
#leaveout = ['V22*', 'V23*', 'V24*', 'V28*', 'V3*', 'V91*, E*']
def isint(string):
    numbers = [str(k) for k in range(10)]
    k=1
    while k < len(string):
        if string[k] in numbers:
            k += 1
        else:
            return False
    return True
    
def wanted(string):
    if '630' < string and string < '67999':
        return False
    if '800' < string and string < '95999':
        return False
    if string[0]=='E':
        return False
    if string[0]=='V':
        if string[1] == '3':
            return False
        if string[1:3] in ['22','23', '24', '28', '91']:
            return False    
    return True

def US_region(member):
    if member['STATE'] in ['WA', 'OR', 'CA', 'NV', 'ID', 'MT', 'WY', 'UT', 'AZ', 'CO', 'NM', 'AK', 'HI']:
        return "West"
    elif member['STATE'] in ['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', 'WI', 'IL', 'IN', 'MI', 'OH']:
        return "Midwest"
    elif member['STATE'] in ['TX', 'OK', 'AR', 'LA', 'KY', 'TN', 'MS', 'AL', 'WV', 'MD', 'DC', 'DE', 'VA', 'NC', 'SC', 'GA', 'FL']:
        return "South"
    elif member['STATE'] in ['PA', 'NJ', 'NY', 'CT', 'RI', 'MA', 'VT', 'NH', 'ME']:
        return "Northeast"
    else:
        return member['STATE']

