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
end module data_handling_module

module filtering_module
  real :: bank_coef = 0.0 !! bank angle - initialised at zero
  real :: num_iter = 1 !! no. of interations - cannot be zero
  real, parameter :: pi=3.1415927 !! pi
  integer :: jj = 1 !! iterator
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

      ! bank slope related coefficient
      bank_coef = 2*sin((90-data(1,5))*(pi/180))

      ! estimate mean flow filter
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
end module filtering_module


program flow
  use data_handling_module
  use filtering_module
  implicit none

  integer, parameter :: nrows = 1000, ncols = 5 , ncols_out = 1

  real :: data(nrows, ncols) !! initialise data array
  real :: flow_meas(nrows, ncols_out), flow_curr(nrows, ncols_out), flow_prev(nrows, ncols_out) !! estimate arrays [m^3/s]

  print *, "Open Channel Flow - Filters"

  call load_data(data, nrows, ncols)
  call mean_filter(data, flow_meas, flow_prev, flow_curr, nrows, ncols, ncols_out)
  call save_data(flow_meas, flow_prev, flow_curr, nrows, ncols_out)

end program flow