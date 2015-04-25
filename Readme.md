This is a working interpreter for the a specific dialect of 'Pseudocode' as used in CS at VT.


#INSTALLATION

Download the files as a zip and at the command line run 
python setup.py install

This will install the pseudo binary and the python tools.


#USAGE

Run pseudo from the command line after installation.

It will open with a blank interpreter:
$> 

Valid bits of pseudocode can be entered here - for example:

$> number N
$> N := 2
$> display N
>> 2
$> display N+5
>> 7
$> list number X
$> X := [1,2,3,4,5]
$> display X[1]
>> 1

All features of pseudocode are implemented. Function calls to the standard library and to algorithms in the current directory work:

Consider the implementation of Euclid's GCD algorithm:

algorithm GCD takes number X, number Y
while  Y != 0
	number temp
	temp := Y
	Y := X % Y
	X := temp 
endwhile
return X

As long as this is in the current directory, it can be called in other scripts as gcd(x,y) (or by the interpreter):

Gregorys-MBP:~ gcolella$ pseudo
$> display gcd(27, 18)
>> 9



#OPTIONS
Verbose modes and trace modes exist (-v and -t respectively).

Verbose execution emits all statements executed (using gcd.pdo from above):

Gregorys-MBP:~ gcolella$ pseudo -v gcd.pdo
Set X? 27
Set Y? 18
  Continuing (Y != 0)                                                      
    Declared number temp                                                   
    temp := 18 (Y)                                                         
    Y := 9 ((X % Y))                                                       
    X := 18 (temp)                                                         
  Continuing (Y != 0)                                                      
    Declared number temp                                                   
    temp := 9 (Y)                                                          
    Y := 0 ((X % Y))                                                       
    X := 9 (temp)                                                          
  Continuing (Y != 0)                                                      
  Returning 9                                                              
Returned 9


Adding the trace option shows all variable values at each step:

Gregorys-MBP:~ gcolella$ pseudo -tv gcd.pdo
Set X? 27
Set Y? 18
  Continuing (Y != 0)                                                      |	X: 27	Y: 18
    Declared number temp                                                   |	X: 27	Y: 18 temp: None
    temp := 18 (Y)                                                         |	X: 27	Y: 18 temp: None
    Y := 9 ((X % Y))                                                       |	X: 27	Y: 18 temp: 18
    X := 18 (temp)                                                         |	X: 27	Y: 9 temp: 18
  Continuing (Y != 0)                                                      |	X: 18	Y: 9
    Declared number temp                                                   |	X: 18	Y: 9 temp: None
    temp := 9 (Y)                                                          |	X: 18	Y: 9 temp: None
    Y := 0 ((X % Y))                                                       |	X: 18	Y: 9 temp: 9
    X := 9 (temp)                                                          |	X: 18	Y: 0 temp: 9
  Continuing (Y != 0)                                                      |	X: 9	Y: 0
  Returning 9                                                              |	X: 9	Y: 0
Returned 9




