! Read in data from file

program read_data
  
  implicit none	

  integer ::  i=0 ! iterator
  integer :: num_points=10 ! no. of measurements
  integer, parameter :: nrows = 1000, ncols = 4
  real :: data(nrows, ncols)

  ! open up and read measurement data
  open(unit=10,file='/home/callum/Desktop/ocf_ukf/ocf_data.csv', action="read", status="old")
  do i=1,nrows
    read(10,*) data(i,:)
    print *, data(i,1), data(i, 2), data(i, 3), data(i, 4)
  end do 
  close(10)

end program read_data