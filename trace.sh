echo 20 | python3 main.py run test/examples/prob5.pyasm --trace tick 2> test/examples/prob5.pyasm.log
echo -e 'foo\n' | python3 main.py run test/examples/cat.pyasm --trace tick 2> test/examples/cat.pyasm.log
python3 main.py run test/examples/hello.pyasm --trace tick 2> test/examples/hello.pyasm.log
python3 main.py run test/examples/cisc.pyasm --trace tick 2> test/examples/cisc.pyasm.log