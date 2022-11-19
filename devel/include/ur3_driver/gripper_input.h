// Generated by gencpp from file ur3_driver/gripper_input.msg
// DO NOT EDIT!


#ifndef UR3_DRIVER_MESSAGE_GRIPPER_INPUT_H
#define UR3_DRIVER_MESSAGE_GRIPPER_INPUT_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace ur3_driver
{
template <class ContainerAllocator>
struct gripper_input_
{
  typedef gripper_input_<ContainerAllocator> Type;

  gripper_input_()
    : DIGIN(0)
    , AIN0(0.0)
    , AIN1(0.0)  {
    }
  gripper_input_(const ContainerAllocator& _alloc)
    : DIGIN(0)
    , AIN0(0.0)
    , AIN1(0.0)  {
  (void)_alloc;
    }



   typedef int32_t _DIGIN_type;
  _DIGIN_type DIGIN;

   typedef double _AIN0_type;
  _AIN0_type AIN0;

   typedef double _AIN1_type;
  _AIN1_type AIN1;





  typedef boost::shared_ptr< ::ur3_driver::gripper_input_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ur3_driver::gripper_input_<ContainerAllocator> const> ConstPtr;

}; // struct gripper_input_

typedef ::ur3_driver::gripper_input_<std::allocator<void> > gripper_input;

typedef boost::shared_ptr< ::ur3_driver::gripper_input > gripper_inputPtr;
typedef boost::shared_ptr< ::ur3_driver::gripper_input const> gripper_inputConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ur3_driver::gripper_input_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ur3_driver::gripper_input_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace ur3_driver

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'ur3_driver': ['/home/ur3/ECE470_Project/src/lab2andDriver/drivers/ur3_driver/msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::ur3_driver::gripper_input_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ur3_driver::gripper_input_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ur3_driver::gripper_input_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ur3_driver::gripper_input_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ur3_driver::gripper_input_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ur3_driver::gripper_input_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ur3_driver::gripper_input_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a4b7d373885d48c37baffd91ce2f1c38";
  }

  static const char* value(const ::ur3_driver::gripper_input_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa4b7d373885d48c3ULL;
  static const uint64_t static_value2 = 0x7baffd91ce2f1c38ULL;
};

template<class ContainerAllocator>
struct DataType< ::ur3_driver::gripper_input_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ur3_driver/gripper_input";
  }

  static const char* value(const ::ur3_driver::gripper_input_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ur3_driver::gripper_input_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int32 DIGIN \n\
float64 AIN0\n\
float64 AIN1\n\
";
  }

  static const char* value(const ::ur3_driver::gripper_input_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ur3_driver::gripper_input_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.DIGIN);
      stream.next(m.AIN0);
      stream.next(m.AIN1);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct gripper_input_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ur3_driver::gripper_input_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ur3_driver::gripper_input_<ContainerAllocator>& v)
  {
    s << indent << "DIGIN: ";
    Printer<int32_t>::stream(s, indent + "  ", v.DIGIN);
    s << indent << "AIN0: ";
    Printer<double>::stream(s, indent + "  ", v.AIN0);
    s << indent << "AIN1: ";
    Printer<double>::stream(s, indent + "  ", v.AIN1);
  }
};

} // namespace message_operations
} // namespace ros

#endif // UR3_DRIVER_MESSAGE_GRIPPER_INPUT_H
