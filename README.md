WARNING: Data is sensitive, if you come across this page please only reference the code.

NOTE: I did not setup pathing configs yet. So manually the scripts: `1_prime_database.py`, `2_run_realtime`, and `fix_image_types.py`. Make sure all of them are absolute paths.

To run:
1. `conda install --yes --file requirements.txt`
2. If you're training more data, delete contents of processed folder, then run `fix_image_types.py`. Else skip this step.
3. Run `1_prime_database.py`, it is stored in `.deepface` (which should be in conda's root).
4. Run `2_run_realtime.py`.

TODO: 
    README: how it each script works, how to configure each.