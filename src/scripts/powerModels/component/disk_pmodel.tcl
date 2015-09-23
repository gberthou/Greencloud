set pModel [new LinearPModel]

set unique_name "disk model"
$pModel set-name $unique_name

$pModel set-coef-number 2
$pModel set-coefficient-numeric "0" 22.32
$pModel set-coefficient "Intercept" 0

if { $printPModel == 1 } {
puts -nonewline "Loaded: Power Model: "
puts $unique_name
}