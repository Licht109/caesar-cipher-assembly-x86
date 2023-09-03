.intel_syntax noprefix

.section .data

wrong_args_message:
.ascii "Wrong amount of args\n"

wrong_args_length:
.long 21

wrong_index_size:
.ascii "Your upper Index is either too big or too small. Please choose one between 0 to 26\n"

wrong_index_size_length:
.long 83

.section .text

.global _start
_start:

.equ LINUX_SYSCALL, 0x80
.equ SYS_EXIT,  1
.equ SYS_WRITE, 4
.equ STDOUT,	1
.equ ABC_SIZE,	26
.equ NEW_LINE, '\n'
.equ ZERO_ASCII, '0'

check_args:
	cmp dword ptr [esp], 3
	jne wrong_args

setup_loop:
	mov ebx, [esp+12]
	xor ecx, ecx
	xor edx, edx

read_loop:
	# find length of the upper index
	inc edx
	cmp BYTE ptr [ebx+edx], 0
	jne read_loop
	cmp edx, 1
	je single_digit
	cmp edx, 2
	je double_digit
	jmp wrong_index

single_digit:
	xor ecx, ecx
	mov cl, BYTE ptr [ebx]
	sub cl, ZERO_ASCII
	mov ebx, ecx
	jmp input_sanity_check

double_digit:
	xor ecx, ecx
	mov cx, WORD ptr [ebx] # get the number
	sub ch, ZERO_ASCII # sub from units 
	sub cl, ZERO_ASCII # sub from tens 
	# we now have the first digit in cl and the second in ch
	# we now preapre to multiply
	xor eax, eax 
	cdq
	mov al, 10
	mul cl
	movzx cx, ch
	add ax, cx
	mov ebx, eax
	jmp input_sanity_check

input_sanity_check:
	test ebx, 0
	jl wrong_index
	cmp ebx, 26
	jg wrong_index
	xor edx, edx # index for loop
	mov eax, [esp+8]

convert_sentence:
	# Actual converting the sentence
	cmp BYTE ptr [eax+edx], 0
	je done_convert

check_lowercase:
	mov cl, BYTE ptr [eax+edx]
	# convert only letters between A-Z-a-z
	sub cl, 'a'
	cmp cl, 'z' - 'a'
	ja check_uppercase
	jmp convert_lowercase

check_uppercase:
	mov cl, BYTE ptr [eax+edx]
	sub cl, 'A'
	cmp cl, 'Z' - 'A'
	ja inc_index
	jmp convert_uppercase

convert_uppercase:
	add BYTE ptr [eax+edx], bl
	# deal with ascii values greater than the in the letters range - uppercase
	cmp BYTE ptr [eax+edx], 'Z'
	jg reset_offset
	jmp inc_index

convert_lowercase:
	add BYTE ptr [eax+edx], bl
	# deal with ascii values greater than the in the letters range - lower calse
	cmp BYTE ptr [eax+edx], 'z'
	ja reset_offset # use unsigned contional jump
	jmp inc_index

reset_offset:
	sub BYTE ptr [eax+edx], ABC_SIZE

inc_index:
	inc edx
	jmp convert_sentence	

done_convert:
	push edx
	push eax
	call print_message
	add esp, 8
	push 1
	push NEW_LINE
	call print_message
	add esp, 8
	jmp exit

wrong_args:
	push wrong_args_length
	push OFFSET FLAT:wrong_args_message
	call print_message
	add esp, 8
   	jmp exit

wrong_index:
	push wrong_index_size_length
   	push OFFSET FLAT:wrong_index_size
	call print_message
	add esp, 8
   	jmp exit

exit:
	mov eax, SYS_EXIT
	xor ebx, ebx
	int LINUX_SYSCALL

.type print_message, @function
print_message:
	push ebp
	mov ebp, esp
	mov eax, SYS_WRITE
	mov ebx, STDOUT
	cmp dword ptr [esp+8], NEW_LINE
	jne print_text
print_newline:
	lea ecx, dword ptr [esp+8]
	jmp end_flow
print_text:
	mov ecx, dword ptr [esp+8]
end_flow:
	mov edx, DWORD ptr [esp+12]
	int LINUX_SYSCALL
	mov esp, ebp
	pop ebp
	ret
