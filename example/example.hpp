class foobar
{
header
    /*
        ^[nam][isEqual]
        ^[cla][foobar]
        ^[des][Returns true if first bar is equal to second bar]
        ^[arg]<bar>[First bar]
        ^[arg]<bar2>[Second bar]
        ^[ret][bool when first bar is equal to second]
    */
    bool isEqual(int bar, int bar2) //header
    {
        return bar == bar2 ? true : false;
    }
    /*
        ^[nam][sum]
        ^[cla][foobar]
        ^[des][Returns sum of bar and bar2]
        ^[arg]<bar>[First bar]
        ^[arg]<bar2>[Second bar]
        ^[ret][sum of both bars in integer type]
    */
    int sum(int bar, int bar2) //header
    {
        return bar + bar2;
    }
}