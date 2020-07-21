program dataread
!
! This program reads in and prints out a name
!
  implicit none
  character *20 :: first_name
  print *, ' type in your first name.'
  print *, ' up to 20 characters'
  read *, first_name
  print *, first_name
end program dataread