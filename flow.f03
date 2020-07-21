! Estimate flow
program flow
  implicit none

  real :: pi = 3.1415927 !! pi
  real :: num_iter = 0 !! no. of interations
  real :: flow_meas !! measured (calculated) flow [m^3/s]
  real, dimension (:), allocatable :: flow_curr, flow_prev !! estimate arrays [m^3/s]
  integer :: i = 1 !! iterator
  integer, parameter :: nrows = 1000, ncols = 5 !! size of data array [nrow x ncols]
  real :: data(nrows, ncols) !! initialise data array
  real :: bank_coef = 0.0

  !! Allocate memory for flow estimates
  allocate (flow_curr(1:nrows)) !! flow array [m^3/s]
  allocate (flow_prev(1:nrows)) !! flow array [m^3/s]

  !! read data from file
  open(unit=10,file='/home/callum/Desktop/ocf_ukf/ocf_data.csv', action="read", status="old")
  do i=1,nrows
    read(10,*) data(i,:) !! [timestamp, height, width, velocity]
  end do 
  close(10)
  
  !! bank slope related coefficient
  bank_coef=2*sin((90-data(i,5))*(pi/180))

  !! estimate flow 
  flow_prev(1) = data(1,4)*(data(1,3)*data(1,2)+bank_coef)
  do i = 1, nrows
    !! increment for gain
    num_iter = num_iter + 1
    !! calculate measured flow
    flow_meas = data(i,4)*(data(i,3)*data(i,2)+bank_coef)
    !! calculate current estimate
    flow_curr(i) = flow_prev(i) + (1/num_iter)*(flow_meas-flow_prev(i))
    ! print *, data(i,1), data(i,2), data(i,3), data(i,4), (flow_meas - flow_prev(i)), (1/num_iter)*(flow_meas - flow_prev(i))

    !! pass current estimates to previous
    if (i + 1 < nrows ) then
      !print *, "Here" , i
      flow_prev(i+1) = flow_curr(i)
      !print *, flow_prev(i+1), flow_curr(i)
    end if

    !! print estimates
    print *, flow_meas, flow_prev(i), flow_curr(i)
  end do

end program flow