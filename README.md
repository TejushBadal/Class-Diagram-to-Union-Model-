# Class-Diagram-to-Union-Model-
This is the code and data set I used to implement my research work on Union Models and UML class diagrams.

Theory:
Under the supervision of Dr. Sanaa Alwidian, my work produced 3 unique contributions to the domain of Model Based Software Engineering as follows:
  - a formal syntax for the abstraction of class diagrams to union models 
  - a union algorithm for the combination of a model family of class diagrams into a union model
  - a graphical user interface for the visualization of the graphs.

Main Components:
- Data set: consists of several class diagrams built using modeling tool 'visual paradigm' exported into a CSV format.
- Union Algorithm: Using python libraries NetworkX and Pandas, I parsed through the information sent by visual paradigm to abstract a class diagram into an attributed                      type graph of just nodes and edges with their respective attributes. I then combined these graphs together to form a Union model to reason about.
