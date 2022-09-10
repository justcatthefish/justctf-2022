# Foreigner

TL;DR: Use PHP's FFI (Foreign Function Interface) to leak process memory.

- Flag is set every 5 or N seconds via `putenv()` (second container/bot; curl will suffice)
- Flag is changed to fake before user input hits `eval()`
- Highly likely, that players will execute `phpinfo()` and discover that FFI is enabled
- Dangerous PHP functions are disabled (to be reviewed); additionally apparmor is applied to the container (getting shell via for ex. CDEF's is not intended)

# TODO:

- Check apparmor profile as it's quick & dirty one (we want to prevent getting shell for ex. via ffi's CDEF's)
- Double check php.ini for disabled functions
