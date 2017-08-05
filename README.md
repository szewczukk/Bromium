<p align="center">
    <img src="/logo.png">
</p>

is simple <a href="https://www.python.org" target="_blank">Python</a> tool to create documentation from C/C++ header files

## Example of Bromium comments in C++
```cpp
    class foobar
    {
        /*
            ^[name][isEqual]
            ^[class][foobar]
            ^[description][Returns true if first bar is qual to second bar]
            ^[argument]<bar>[First bar]
            ^[argument]<bar2>[Second bar]
            ^[retutns][bool when first bar is equal to second]
        */
        bool isEqual(int bar, int bar2) //^header
        {
            return bar == bar2 ? true : false;
        }
        //^[start]
        //^[cla][foobar]
        //^[des][Returns sum of bar and bar2]
        //^[arg]<bar>[First bar]
        //^[arg]<bar2>[Second bar]
        //^[ret][sum of both bars in integer type]
        int sum(int bar, int bar2) //^header
        {
            return bar + bar2;
        }
    };
```

## Installation
Just clone this repository at your project catalog

    $ git clone https://github.com/bjornus/bromine
  
## How to  use
Run Bromine Python file

    $ python bromine.py

or

    $ chmod +x bromine.py
    $ ./bromine.py
    
Choose relative to this path of header files (eg. headers/)
    
    $ headers/
    
Choose extension of files (e.g *.hpp)
    
    $ .hpp

Choose directory to catalog in witch Bromine have to create HTML files

    $ output/

And your documentation is ready! Just look into output directory

## Pattern of comments
<table>
    <tr>
        <td>
            <b>Name of method</b> 
        </td>
        <td>
            [nam][name of method]
        </td>
   </tr>
   <tr>
        <td>
            <b>Name of class where method is</b> 
        </td>
        <td>
            [cla][Name]
        </td>
    </tr>
    <tr>
        <td>
           <b>Description</b> 
        </td>
        <td>
            [des][description fo method]
        </td>
     </tr>
     <tr>
        <td>
            <b>Arguments</b> 
        </td>
        <td>
            [arg]&lt;name&gt;[description of argument]
        </td>
    </tr>
    <tr>
        <td>
            <b>Returns</b> 
        </td>
        <td>
            [ret][description of returning value]
        </td>
    </tr>
</table>

## Comments
* All Bromium comments start with ^ symbol
* Add comment //headers after headers of method
* Clone this repository in catalog where is all header files or down in hierarchy
* To change template of HTML file or modificate CSS, modify templates.xml in .bromine catalog
* Don't close HTML tags in .bromine/templates.xml file, those tags will be added in script
* If you want to create documentation comments in C/C++ file, use ALL of available comment types (table on top of README)
* To set new settings without deleting settings file, add "new" argument when you call bromine.py file (python bromine.py new)
* To modify page templates, add argument "modify" to calling bromine.py file
* If there is couple of methods with same name, give them different names in comments

## Licensing
To see the license of Bromine, open <a href="https://github.com/bjornus/bromium/blob/master/LICENSE" target="_blank">LICENSE</a> file.
