 BEGIN {file = 1; filename = "mode_"  file ".pdb"}
 /ENDMDL/ {getline; file ++; filename = "mode_" file ".pdb"}
 {print $0 > filename}