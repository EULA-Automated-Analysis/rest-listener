from models.heuristic import Heuristic
from flask import Flask
import urllib
import urllib2
import os
import json

# Keys are specified in https://developers.google.com/webmaster-tools/search-console-api/reference/rest/v1/urlTestingTools.mobileFriendlyTest/run#MobileFriendlyIssue
grade_ratios = {
    'MOBILE_FRIENDLY_RULE_UNSPECIFIED': 0,
    'USES_INCOMPATIBLE_PLUGINS': 0,
    'CONFIGURE_VIEWPORT': 3,
    'FIXED_WIDTH_VIEWPORT': 5,
    'SIZE_CONTENT_TO_VIEWPORT': 5,
    'USE_LEGIBLE_FONT_SIZES': 10,
    'TAP_TARGETS_TOO_CLOSE': 2
}

grades = ['F', 'D', 'C', 'B', 'A']

# Procedural 1b
# Ensure readability of EULA on mobile devices
class MobileReadability(Heuristic):

    @staticmethod
    def score(eula):
        # Create string keyed dictionary for conversion into JSON at end
        ret_vals = {
            'name': 'Mobile Readability',
            'description': 'Assesses the readability of a EULA on a web-page',
            'max': 4
        }

        if eula.url is None:
            ret_vals['reason'] = 'no url'
            ret_vals['score'] = -1
            ret_vals['grade'] = 'N/R'
            return ret_vals

        # Fetch API key from env var
        # If key does not load, omit this heuristic
        if 'google_api_key' not in os.environ:
            ret_vals['reason'] = 'Could not connect to Google APIs (NOKEY)'
            ret_vals['score'] = -1
            ret_vals['grade'] = 'N/R'
            return ret_vals

        try:
            google_api_key = os.environ['google_api_key']
            service_url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'

            # Parameters to send to google URL
            params = {
                'url': eula.url,
                'key': google_api_key
            }

            # Open connection and read data back
            content = json.loads(urllib2.urlopen(url=service_url, data=urllib.urlencode(params)).read())

            # Make sure test ran properly
            if content['testStatus']['status'] != 'COMPLETE':
                ret_vals['reason'] = 'Could not connect to Google APIs (NOKEY)'
                ret_vals['score'] = -1
                ret_vals['grade'] = 'N/R'
                return ret_vals

            # If there are no issues or no reason to deduct (might be redundent, but is safer way to reference api), return our score
            if content['mobileFriendliness'] == "MOBILE_FRIENDLY" or 'mobileFriendlyIssues' not in content:
                ret_vals['reason'] = 'Could not connect to Google APIs (NOKEY)'
                ret_vals['score'] = 4
                ret_vals['grade'] = grades[4]
                return ret_vals

            # If there are issues
            if 'mobileFriendlyIssues' in content:
                # Extract issues into a single array
                issues = map(lambda x: x['rule'], content['mobileFriendlyIssues'])
                # Start by considering the entire denominator
                denom = sum(grade_ratios.values())
                num = float(denom)

                # Subtract from numerator for each issue, relative to the weights at top
                for issue in issues:
                    num = num - grade_ratios[str(issue)]

                # Multiply score by 4 for our even representation
                ret_vals['score'] = int(round(4 * num / denom))
                # Assign grade to score
                ret_vals['grade'] = grades[ret_vals['score']]

                # Add issues to the return score if we have them
                if len(issues) > 0:
                    ret_vals['issues'] = issues

                # Make final return call
                return ret_vals

        except urllib2.URLError:
            ret_vals['score'] = -1
            ret_vals['grade'] = 'N/R'
            ret_vals['reason'] = 'Could not connect to Google APIs'
            return ret_vals
        except KeyError:
            ret_vals['score'] = -1
            ret_vals['grade'] = 'N/R'
            ret_vals['reason'] = 'Error parsing Google API Result'
            return ret_vals
