# documentator

is simple <a href="https://www.python.org" target="_blank">Python</a> tool to create documentation from C/C++ header files

## Installation
Just clone this repository at your project catalog

    $ git clone https://github.com/bjornus/documentator
  
## How to  use
Run main Python file

    $ python main.py
    
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
            [nam][calcPi]
        </td>
   </tr>
   <tr>
        <td>
            <b>Name of class where method is</b> 
        </td>
        <td>
            [cla][MathClass]
        </td>
    </tr>
    <tr>
        <td>
           <b>Description</b> 
        </td>
        <td>
            [des][Calculating Pi number]
        </td>
     </tr>
     <tr>
        <td>
            <b>Arguments</b> 
        </td>
        <td>
            [arg][a - First argument ; b - Second argument]
        </td>
    </tr>
    <tr>
        <td>
            <b>Returning</b> 
        </td>
        <td>
            [ret][Pi number as delta]
        </td>
    </tr>
</table>

## Comments
* Clone this repository in catalog where is all header files or down in hierarchy
* To change template of HTML file or modificate CSS, modify files in utils catalog
* Don't close HTML tags in utils/raw.html file, those tags will be added in script

## Licensing
To see the license of documentator, open <a href="https://github.com/bjornus/documentator/blob/master/LICENSE" target="_blank">LICENSE</a> file.
