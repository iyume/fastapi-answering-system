## Schedule
- [x] initial usable jwt-cookie-authorization (not OAuth2 inner) in front and rear separation constructure
- [x] initial usable random question-select practice, and click option to render an answer page
- [x] all functional page complete

## TODO
**backend**
- [ ] add unitest for api
- [ ] save user wrong answer for analysis
- [ ] add block user api
- [ ] add retrieve password function

**frontend**
- [x] improve old template pattern
- [x] complete login action and add login_required for router
- [x] add exam page
- [x] logout utility
- [ ] use Redis to store user refresh token and replace `one-token` pattern

## Known Bugs
- path_params contains space like `?tag=test%20tag` will be redirect as `?tag=test+tag` which do not urldecode, will turn to a wrong page
