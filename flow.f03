!###################################################################################
!# Author: Callum Tyler 2020
!#
!### Description:
!# This program estimates Open Channel Flow [m^3/s] estimated for using a 1D kalman filter.
!# 
!### Instructions:
!# Compile with: `gfortran flow.f03 -o flow`
!# Run with: `./flow`
!#
!###################################################################################

program flow
  implicit none
  !! initialise constants, variables, arrays
  integer :: ui_in = 10, ui_out = 11 !! handles for I/O if files
  real :: pi = 3.1415927 !! pi
  real :: num_iter = 1 !! no. of interations - cannot be zero
  integer :: i = 1 !! iterator
  integer, parameter :: nrows = 1000, ncols = 5 , ncols_out = 1 !! size of data array [nrow x ncols]
  real :: data(nrows, ncols) !! initialise data array
  real :: flow_meas(nrows, ncols_out), flow_curr(nrows, ncols_out), flow_prev(nrows, ncols_out) !! estimate arrays [m^3/s]
  real :: bank_coef = 0.0 !! bank coefficient

  !! read data from file
  open(unit=ui_in,file='/home/callum/Desktop/ocf_kf/data/ocf_data.csv', action="read", status="old")
  do i=1,nrows
    read(ui_in,*) data(i,:) !! [timestamp, height, width, velocity]
  end do 
  close(ui_in)
  
  !! bank slope related coefficient
  bank_coef=2*sin((90-data(1,5))*(pi/180))

  !! estimate flow filter
  flow_prev(1,1) = data(1,4)*(data(1,3)*data(1,2)+bank_coef)
  do i = 1, nrows
    !! increment for gain
    num_iter = num_iter + 1
    !! calculate measured flow
    flow_meas(i,1) = data(i,4)*(data(i,3)*data(i,2)+bank_coef)
    !! calculate current estimate
    flow_curr(i,1) = flow_prev(i,1) + (1/num_iter)*(flow_meas(i,1)-flow_prev(i,1))
    ! print *, data(i,1), data(i,2), data(i,3), data(i,4), (flow_meas - flow_prev(i)), (1/num_iter)*(flow_meas - flow_prev(i))

    !! pass current estimates to previous
    if (i + 1 < nrows ) then
      !print *, "Here" , i
      flow_prev(i+1,1) = flow_curr(i,1)
      !print *, flow_prev(i+1), flow_curr(i)
    end if
  end do

  !! save estimates - write over last file
  open(unit=ui_out,file='/home/callum/Desktop/ocf_kf/data/ocf_flow_meas.csv', action="write")
  do i=1,nrows 
    write(ui_out,*) flow_meas(i,1)
  end do 
  close(ui_out)

  open(unit=ui_out,file='/home/callum/Desktop/ocf_kf/data/ocf_flow_prev.csv', action="write")
  do i=1,nrows 
    write(ui_out,*) flow_prev(i,1)
  end do 
  close(ui_out)

  open(unit=ui_out,file='/home/callum/Desktop/ocf_kf/data/ocf_flow_curr.csv', action="write")
  do i=1,nrows 
    write(ui_out,*) flow_curr(i,1)
  end do 
  close(ui_out)

end program flow