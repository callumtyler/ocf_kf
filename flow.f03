! Estimate flow
program flow
  implicit none

  real :: flow_est ! water flow [m^3/s]
  real :: initial_flow ! initial flow [m^3/s]
  real :: velocity = 0.5 ! water speed [m/s]
  real :: bank_angle = 35 ! bank angle, measured from horizon (deg)
  real :: water_depth = 2.0 ! water depth [m]
  real :: channel_width = 20 ! base channel width [m]
  real :: pi = 3.1415927 ! pi
  real, dimension (:), allocatable :: height_meas ! water depth mesurements [m]
  real, dimension (:), allocatable :: flow_meas ! flow estimates [m^3/s]
  integer :: num_meas = 5 ! number of measurements
  integer :: i ! iterator
  real :: height_prev = 1.0 ! previous height [m]

  allocate (height_meas(1:num_meas))
  allocate (flow_meas(1:num_meas))

  do i = 0, num_meas
    height_meas(i) = height_prev + 0.1
    height_prev = height_meas(i)
    !print *, height_meas(i)
  end do

  do i = 0, num_meas
    flow_meas(i) = velocity * (channel_width * height_meas(i) + 2 * sin(pi*(90 - bank_angle)/180))
    print *, flow_meas(i)
  end do
 
end program flow