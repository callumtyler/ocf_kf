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
!### Design Questions:
!# Why use subroutine? Means that no need to handle passing variables to/from "functional code".
!#
!###################################################################################

module data_handling_module
  integer, parameter :: ui=10 !! file i/o unit number
  integer :: ii = 1 !! iterator
  contains
    !! load_data subroutine
    subroutine load_data(data, nrows, ncols)
      integer, intent (in) :: nrows
      integer, intent (in) :: ncols
      real, intent (inout) :: data(nrows, ncols)

      print *, " --> Loading Data -->"

      !! read data from file
      open(unit=ui,file='/home/callum/Desktop/ocf_kf/data/ocf_data.csv', action="read", status="old")
      do i=1,nrows
        read(ui,*) data(i,:) !! read all columns row-by-row [timestamp, height, width, velocity]
      end do 
      close(ui) !! close file
    end subroutine load_data

    !! save_data subroutine
    subroutine save_data(flow_meas, flow_prev, flow_curr, nrows, ncols_out)
      integer, intent (in) :: nrows
      integer, intent (in) :: ncols_out
      real, intent (in) :: flow_meas(nrows, ncols_out)
      real, intent (in) :: flow_prev(nrows, ncols_out)
      real, intent (in) :: flow_curr(nrows, ncols_out)
      print *, " <-- Saving data <--"
      !! save estimates - write over last file
      open(unit=ui,file='/home/callum/Desktop/ocf_kf/data/ocf_flow_meas.csv', action="write")
      do ii=1,nrows 
        write(ui,*) flow_meas(ii,ncols_out) !! write data row-by-row
      end do 
      close(ui) !! close file

      open(unit=ui,file='/home/callum/Desktop/ocf_kf/data/ocf_flow_prev.csv', action="write")
      do ii=1,nrows 
        write(ui,*) flow_prev(ii,ncols_out) !! write data row-by-row
      end do 
      close(ui) !! close file

      open(unit=ui,file='/home/callum/Desktop/ocf_kf/data/ocf_flow_curr.csv', action="write")
      do ii=1,nrows 
        write(ui,*) flow_curr(ii,ncols_out) !! write data row-by-row
      end do 
      close(ui) !! close file
    end subroutine save_data

    subroutine load_parameters(nrows, uncert_curr, uncert_prev, uncert_meas, type_filter)
      real, intent (inout) :: uncert_curr
      real, intent (inout) :: uncert_prev
      real, intent (inout) :: uncert_meas
      integer, intent (inout) :: nrows
      integer, intent (inout) :: type_filter
      print *, "--> Loading parameters -->"
      open(unit=ui,file='/home/callum/Desktop/ocf_kf/flow_parameters.txt', action="read")
      read(ui,*) nrows
      read(ui,*) uncert_curr
      read(ui,*) uncert_prev
      read(ui,*) uncert_meas
      read(ui,*) type_filter
      close(ui)
    end subroutine load_parameters
end module data_handling_module

module filtering_module
  real :: bank_coef = 0.0 !! bank angle - initialised at zero
  real :: num_iter = 1 !! no. of interations - cannot be zero
  real, parameter :: pi=3.1415927 !! pi
  integer :: jj = 1 !! iterator
  real :: kalman_gain = 1.0 !! Kalman gain
  real :: uncert_temp = 1.0 !! temporary uncertainty variable
  contains
    subroutine mean_filter(data, flow_meas, flow_prev, flow_curr, nrows, ncols, ncols_out)
      integer, intent (in) :: nrows
      integer, intent (in) :: ncols
      integer, intent (in) :: ncols_out
      real, intent (in) :: data(nrows, ncols)
      real, intent (inout) :: flow_meas(nrows, ncols_out)
      real, intent (inout) :: flow_prev(nrows, ncols_out)
      real, intent (inout) :: flow_curr(nrows, ncols_out)

      print *, " % Running mean filter %"

      !! bank slope related coefficient
      bank_coef = 2*sin((90-data(1,5))*(pi/180))

      !! estimate mean flow filter
      flow_prev(1,1) = data(1,4)*(data(1,3)*data(1,2)+bank_coef)
      do jj = 1, nrows
        !! increment for gain
        num_iter = num_iter + 1
        !! calculate measured flow
        flow_meas(jj,1) = data(jj,4)*(data(jj,3)*data(jj,2)+bank_coef)
        !! calculate current estimate
        flow_curr(jj,1) = flow_prev(jj,1) + (1/num_iter)*(flow_meas(jj,1)-flow_prev(jj,1))

        !! pass current estimates to previous
        if (jj + 1 < nrows ) then
          flow_prev(jj+1,1) = flow_curr(jj,1)
        end if
      end do
    end subroutine mean_filter

    subroutine kalman_filter(data, flow_meas, flow_prev, flow_curr, nrows, ncols, ncols_out, uncert_prev, uncert_meas, uncert_curr)
      real, intent (inout) :: uncert_curr
      real, intent (inout) :: uncert_prev
      real, intent (inout) :: uncert_meas
      integer, intent (in) :: nrows
      integer, intent (in) :: ncols
      integer, intent (in) :: ncols_out
      real, intent (in) :: data(nrows, ncols)
      real, intent (inout) :: flow_meas(nrows, ncols_out)
      real, intent (inout) :: flow_prev(nrows, ncols_out)
      real, intent (inout) :: flow_curr(nrows, ncols_out)

      print *, " % Running kalman filter %"

      !! bank slope related coefficient
      bank_coef = 2*sin((90-data(1,5))*(pi/180))
      !! calculate initial kalman gain
      kalman_gain = uncert_prev/(uncert_prev-uncert_meas)

      do jj = 1, nrows
        !! calculate measured flow
        flow_meas(jj,1) = data(jj,4)*(data(jj,3)*data(jj,2)+bank_coef)
        !! calculate current estimate
        flow_curr(jj,1) = flow_prev(jj,1) + kalman_gain*(flow_meas(jj,1)-flow_prev(jj,1))

        !! pass current estimates to previous
        if (jj + 1 < nrows ) then
          flow_prev(jj+1,1) = flow_curr(jj,1)
        end if

        !! temporarily store uncert_curr
        uncert_temp = uncert_curr

        !! recalculate/update uncert_curr for next iteration
        uncert_curr = (1 - kalman_gain)*uncert_prev

        !! push current to prev for next iteration
        uncert_prev = uncert_temp

        !! recalculate/update kalman gain for next iteration
        kalman_gain = uncert_prev/(uncert_prev-uncert_meas)
      end do
    end subroutine kalman_filter
end module filtering_module


program flow
  use data_handling_module
  use filtering_module
  implicit none

  !! define & initialise variables and constants
  integer, parameter :: ncols = 5 , ncols_out = 1, nrows = 1000
  integer :: type_filter = 0 
  real :: uncert_prev = 0.09, uncert_meas = 0.001, uncert_curr = 0.1  

  print *, "Open Channel Flow - Filters"

  call load_parameters(uncert_curr, uncert_meas, uncert_prev, type_filter)
  
  real :: data(nrows, ncols) !! initialise data array
  ! estimate arrays [m^3/s]
  real :: flow_meas(nrows, ncols_out), flow_curr(nrows, ncols_out), flow_prev(nrows, ncols_out) 

  call load_data(data, nrows, ncols)

  if (type_filter == 1) then

    call mean_filter(data, flow_meas, flow_prev, flow_curr, nrows, ncols, ncols_out)

  else if (type_filter == 2) then

    call kalman_filter(data, flow_meas, flow_prev, flow_curr, nrows, ncols, ncols_out, uncert_prev, uncert_meas, uncert_curr)

  else

    print *, "Not an option!"

  end if

  call save_data(flow_meas, flow_prev, flow_curr, nrows, ncols_out)

end program flow