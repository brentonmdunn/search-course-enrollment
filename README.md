# Search Course Enrollment

This is a command line application that is based on data from [UCSD Historical Enrollment Data](https://github.com/UCSD-Historical-Enrollment-Data). The goal is to make it faster to see when courses filled up. If a course fills up, the program returns the time, the class standing level, and which pass.

It currently only supports Fall 2022 and Winter 2023. Press <b>q</b> to quit.

## Download
```
git clone https://github.com/brentonmdunn/search-course-enrollment.git
cd search-course-enrollment
python3 main.py
```


## Future Plans
- Add remaining quarters that have data
- Add full Docker capabilities
- Add suggestions for similar courses for typos
- Account for CSE priority
- Account for freshmen fall enrollment
