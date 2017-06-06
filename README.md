# documentator

is simple <a href="https://www.python.org" target="_blank">Python</a> tool to create documentation from C/C++ header files

## Example of documentator comments in C++
```cpp
    class foobar
    {
        /*
            ^[nam][isEqual]
            ^[cla][foobar]
            ^[des][Returns true if first bar is qual to second bar]
            ^[arg]<bar>[First bar]
            ^[arg]<bar2>[Second bar]
            ^[ret][bool when first bar is equal to second]
        */
        bool isEqual(int bar, int bar2) //^header
        {
            return bar == bar2 ? true : false;
        }
        //^[nam][sum]
        //^[cla][foobar]
        //^[des][Returns sum of bar and bar2]
        //^[arg]<bar>[First bar]
        //^[arg]<bar2>[Second bar]
        //^[ret][sum of both bars in integer type]
        int sum(int bar, int bar2) //^header
        {
            return bar + bar2;
        }
    }
```

## Installation
Just clone this repository at your project catalog

    $ git clone https://github.com/bjornus/documentator
  
## How to  use
Run documentator Python file

    $ python documentator.py

or

    $ chmod +x documentator.py
    $ ./documentator.py
    
Choose relative to this path of header files (eg. headers/)
    
    $ headers/
    
Choose extension of files (e.g *.hpp)
    
    $ .hpp

Choose directory to catalog in witch documentator have to create HTML files

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
            [arg]<name>[description of argument]
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
* All documentator comments start with ^ symbol
* Add comment //headers after headers of method
* Clone this repository in catalog where is all header files or down in hierarchy
* To change template of HTML file or modificate CSS, modify templates.xml in .documentator catalog
* Don't close HTML tags in .documentator/templates.xml file, those tags will be added in script
* If you want to create documentation comments in C/C++ file, use ALL of available comment types (table on top of README)
* To set new settings without deleting settings file, add "new" argument when you call documentator.py file (python documentator.py new)
* To modify page templates, add argument "modify" to calling documentator.py file

## Licensing
To see the license of documentator, open <a href="https://github.com/bjornus/documentator/blob/master/LICENSE" target="_blank">LICENSE</a> file.
