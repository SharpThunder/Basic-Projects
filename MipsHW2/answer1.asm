.data 
list_A: .word
.text
la $s0, list_A    # based address of list A loaded into $s0
addi $s1, $zero, 582

# Continue to write your code here

addi $t0,$t0,5
add $t2,$s1,$zero
addi $t1,$s0,0
loop:slt $t3,$t2,$t0
bne $t3,$zero,end
div $t2,$t0
mflo $t2
mfhi $t4
sw $t4,0($t1)
addi $t1,$t1,4
j loop
end:
sw $t2,0($t1)
