// Clock crossings: a register named *_meta is the first stage of a synchronizer (iosys's
// UART input, usb_hid_sync's USB buttons). The path into it crosses clocks on purpose.
set_false_path -to [get_regs {*_meta*}]
