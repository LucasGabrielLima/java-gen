run:
	python3 src/javagen.py examples/ex1.json output

build:
	python3 src/javagen.py examples/ex1.json output
	javac *.java

clean:
	rm *.class *.java