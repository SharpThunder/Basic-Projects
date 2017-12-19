#Lists are defined here
.data
my_data: .word 1, 3, 6, 7
my_data2: .word 2, 1, 5

.text
la $s0, my_data    # based address of list A loaded into $s0
addi $s1, $zero, 4  # $s1 is set to the size of the my_data
la $s2, my_data2      # based address of list B loaded into $s2
addi $s3, $zero, 3  # $s3 is set to the size of the my_data2


# Continue to write your code here

addi $t3,$s0,0 #baseadress my_data
addi $t4,$t4,0 #i
loop:
beq $s1,$t4,exit
lw $t5,0($t3)
addi $a0,$t5,0
jal sum
sw $v0,0($t3)
addi $t3,$t3,4
addi $t4,$t4,1
j loop

exit:
addi $t6,$s2,0 #baseadress my_data2
addi $t7,$t7,0 #i
loop2:
beq $s3,$t7,exit2
lw $t8,0($t6)
addi $a0,$t8,0
jal sum
sw $v0,0($t6)
addi $t6,$t6,4
addi $t7,$t7,1
j loop2

exit2:

sum:
addi $t0,$t0,0 #sum
addi $t1,$a0,0 #x
addi $t2,$t2,0 #i
loop3:
beq $t1,$t2,exit3
add $t0,$t0,$t1
addi $t2,$t2,1
j loop3
exit3:
add $v0,$t0,$zero
jr $ra



