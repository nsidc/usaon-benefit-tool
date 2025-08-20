## v2.5.0 (2025-08-19)

* Allow more linking capabilities for data products
* Update criticality key
* Improve assessment download table
* Add search option when adding node to assessment

## v2.4.1 (2025-03-04)

* Make null criticality line thicker
* Hide private field on assessments

## v2.4.0 (2024-10-11)

* Update SBA framework
    * Multiple DB migrations (final migration (ce8e6e308e5c))
    * No longer prefill information
    * Add fields for framework information
* Allow linking between observation system and application nodes

## v2.3.0 (2024-10-02)

* Add sort functionality to assessments and object library pages
* Allow null performance and criticality ratings on links (db migration ea1181510e10)
    * Null performance is displayed as gray
    * Null criticality is displayed as a thin line
* Display a legend for criticality rating


## v2.2.0 (2024-10-01)

* Allow nodes of same type to link.
* Reverse color bar.
* Add new link fields (db migration 925ed377e31b).

## v2.1.0 (2024-09-26)

* Increase length of description columns to 4096 chars (db migration fafa3da67d5e).


## v2.0.2 (2024-06-07)

* Change all sankey nodes to gray color.


## v2.0.1 (2024-03-21)

* Bugfix: Remove obsolete template import.


## v2.0.0 (2024-03-21)

* Revamp data model
    * All objects unified in one main table
    * Renamed surveys/projects -> Assessments
    * Added object library table
* Revamp user experience
    * Enter assessment data all on one page
    * Manage object library separately from assessment data
* Revamp architecture
    * Use HTMX to start implementing HATEOAS architecture
* New features
    * Assessments can be private (only visible to Admins)
    * Detailed tooltips on Sankey diagram


## v1.6.1 (2023-12-22)

* Spelling fixes


## v1.6.0 (2023-12-21)

* Standardize all create/edit/delete buttons
* Refer to "Surveys" as "Projects" in the user interface
    * This is a temporary change for user testing, see #228 for long-term
      decision-making


## v1.5.0 (2023-12-21)

* Adopt a suitable webserver for production: Gunicorn


## v1.4.1 (2023-12-20)

* Bugfix: Fix permission error when analysts view user guide


## v1.4.0 (2023-12-20)

* More consistent datetime display format
* Remove table borders
* Improve some user interface element label text


### Survey pages user experience enhancements

* **Remove the confusing concept of "response" from the UI**
* Overhaul navigation of survey data entry
* Add markdown `user_guide.md` template for accessible editing
* Minor UI adjustments:
    * Hide some noisy survey info under a tooltip
    * More consistent button style
* Survey listing:
    * Make some columns admin-only
    * Re-order columns for readability


## v1.3.0 (2023-12-19)

### Survey page user experience enhancements

* Style informational text as Bootstrap "Alerts"
* Improve UI of survey & surveys pages
* Add sankey diagram display to survey page


### Login user experience enhancements

* Display banner when not logged in.
* New login page with button to let user know we're using Google SSO.
	We can add more provider here later.
* When accessing restricted routes, redirect to login page.
		* After a successful login, users will be redirected to the restricted
			route they tried to access earlier.


## v1.2.0 (2023-12-18)

### Bug fixes

* Fix login redirect misbehaviors (#178, #58)


### Other

* Add docs site (#201, #202, #203)
* Finish renaming -> Benefit Tool (#204)
* Apply Cosmo bootswatch theme, adjust layout (#209)
* Add mechanism to render Markdown in templates (#208)
* Modernization (#207)


## v1.1.0 (2023-11-01)

* Add description and links to the home page that will help users navigate the site


## v1.0.2 (2023-10-26)

* Bugfix: allow non-admin users to edit their profiles


## v1.0.1 (2023-10-16)

* Fix link on home page
* Update VTA to Benefit tool in more places


## v1.0.0 (2023-10-15)

* Enable deleting response objects/cascading deletes


## v0.8.0 (2023-10-12)

* Enable deleting relationships


## v0.7.1 (2023-10-10)

* Bugfix: proxy redirect for new survey


## v0.7.0 (2023-10-09)

* Bugfix: proxy redirect for login/logout
* Update DB for analyst to be default role


## v0.6.0 (2023-10-06)

* Create citation/zenodo tag
* Block new response objects being created by analyst
* Show sankey previews on all relationship pages
* Show full sankey preview on response home page


## v0.5.0 (2023-10-03)

* Bugfix relationship creation
* Fix envarrs for google login/non dev environment


## v0.4.1 (2023-09-13)

* Bugfix environment variables


## v0.4.0 (2023-09-13)

* Stop using current_user and use true value for created_by on surveys page
* Display version on webapp
* Combine common response object database fields
* Show respondents on survey page
* Install bootstrap and update UI
* Update response link to be clickable
* Implement X-forwarded-proxy


## v0.3.0 (2023-08-17)

* Set up/improve all relationship interfaces
* Populate societal benefit area reference data
* Implement role dropdown on profile page

## v0.2.1 (2023-08-10)

* Temporary https fix


## v0.2.0 (2023-08-09)

* Create user list view
* Allow role changes by admin
* Add analyst and respondent roles
* Redirect to homepage after login
* Alter views based on roles


## v0.1.1 (2023-07-26)

* Set up "ad-hoc" HTTPS cert for dev


## v0.1.0 (2023-07-26)

* Initial release
