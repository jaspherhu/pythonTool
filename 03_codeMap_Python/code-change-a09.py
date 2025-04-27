# -*- coding: utf-8 -*-

# 系统相关导入
import os
import sys
import platform

# 时间和随机数相关导入
import random
import collections
from datetime import datetime

# 文件处理相关导入
import json
import csv
import chardet
import shutil

# 字符串处理相关导入
import string
import re

# GUI相关导入
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 线程相关导入
import threading
# ... existing code ...

# 新增配置路径常量
MAPPING_CONFIG_PATH = 'mapping_config.json'
VERSION = "20250302"
# 新增全局常量：关键字最小长度
MIN_KEYWORD_LENGTH = 8

# 新增：C语言关键词列表
C_KEYWORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'inline', 'int', 'long', 'register', 'restrict', 'return', 'short',
    'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
    'unsigned', 'void', 'volatile', 'while', '_Bool', '_Complex', '_Imaginary',
    'memset', 'strcat', 'strcmp', 'strcpy', 'strlen', 'strncat', 'strncmp',
    'strncpy', 'strstr', 'strtok', 'strtol', 'strtoul', 'strtod', 'strtof',
    'strtold', 'strtoll', 'strtoull', 'strerror', 'strsignal', 'strcoll',
    'strxfrm', 'memchr','memcmp', 'memcpy', 'memmove', 'memccpy',
    'uint16_t', 'uint8_t', 'uint32_t', 'uint64_t', 'int8_t', 'int16_t', 'int32_t', 'int64_t',
    'defined', '__func__', '__FILE__', '__LINE__', '__DATE__', '__TIME__', 'define',
    '__attribute__', '__builtin__', '__inline__', '__restrict__', '__signed__', '__volatile__',
    '__asm__', 'control',
    'sprintf', 'printf', 'scanf', 'atoi', 'atof', 'atol', 'atoll',
    'localtime', 'tm_mon', 'tm_mday', 'tm_year', 'tm_hour', 'tm_min', 'tm_sec', 'mktime',
    'malloc', 'free', 'calloc', 'realloc', 'osDelay',
    'va_start', 'va_end','vsnprintf', 'snprintf' 
}

EXCLUDED_IDENTIFIERS = {
    # 1. C++11 Standard Library Identifiers (More comprehensive)
    # Containers & Adapters
    'array', 'vector', 'deque', 'forward_list', 'list', 'stack', 'queue', 'priority_queue',
    'set', 'map', 'multiset', 'multimap', 'unordered_set', 'unordered_map', 'unordered_multiset', 'unordered_multimap',
    # Iterators & Utilities
    'iterator', 'begin', 'end', 'cbegin', 'cend', 'rbegin', 'rend', 'crbegin', 'crend',
    'pair', 'tuple', 'get', 'make_pair', 'make_tuple', 'tie',
    'initializer_list',
    # Memory Management
    'allocator', 'allocator_traits', 'pointer_traits',
    'unique_ptr', 'shared_ptr', 'weak_ptr', 'make_unique', 'make_shared', 'enable_shared_from_this',
    'owner_less', 'bad_weak_ptr',
    # Input/Output Streams
    'ios', 'streambuf', 'istream', 'ostream', 'iostream',
    'stringbuf', 'istringstream', 'ostringstream', 'stringstream',
    'filebuf', 'ifstream', 'ofstream', 'fstream',
    'cin', 'cout', 'cerr', 'clog', 'wcin', 'wcout', 'wcerr', 'wclog',
    'endl', 'flush', 'ws', 'showbase', 'showpoint', 'showpos', 'uppercase', 'nouppercase',
    'boolalpha', 'noboolalpha', 'fixed', 'scientific', 'hexfloat', 'defaultfloat', 'internal', 'left', 'right',
    'dec', 'hex', 'oct', 'setbase', 'setfill', 'setprecision', 'setw',
    'get_money', 'put_money', 'get_time', 'put_time',
    # Strings & Text Processing
    'string', 'wstring', 'u16string', 'u32string', 'basic_string',
    'char_traits', 'stoi', 'stol', 'stoul', 'stoll', 'stoull', 'stof', 'stod', 'stold', 'to_string', 'to_wstring',
    'regex', 'regex_match', 'regex_search', 'regex_replace', 'smatch', 'cmatch', 'wsmatch', 'wcmatch', 'sub_match',
    'regex_iterator', 'regex_token_iterator', 'regex_error', 'regex_constants',
    # Algorithms & Numerics
    'algorithm', 'numeric', 'functional', 'ratio', 'complex', 'valarray',
    'sort', 'stable_sort', 'partial_sort', 'partial_sort_copy', 'is_sorted', 'is_sorted_until',
    'find', 'find_if', 'find_if_not', 'find_end', 'find_first_of',
    'adjacent_find', 'count', 'count_if', 'mismatch', 'equal', 'is_permutation', 'search', 'search_n',
    'copy', 'copy_if', 'copy_n', 'copy_backward', 'move', 'move_backward',
    'fill', 'fill_n', 'transform', 'generate', 'generate_n', 'remove', 'remove_if', 'remove_copy', 'remove_copy_if',
    'replace', 'replace_if', 'replace_copy', 'replace_copy_if', 'swap', 'swap_ranges', 'iter_swap',
    'reverse', 'reverse_copy', 'rotate', 'rotate_copy', 'shuffle', 'unique', 'unique_copy',
    'lower_bound', 'upper_bound', 'equal_range', 'binary_search',
    'merge', 'inplace_merge', 'includes', 'set_union', 'set_intersection', 'set_difference', 'set_symmetric_difference',
    'push_heap', 'pop_heap', 'make_heap', 'sort_heap', 'is_heap', 'is_heap_until',
    'min', 'max', 'minmax', 'min_element', 'max_element', 'minmax_element', 'lexicographical_compare',
    'accumulate', 'inner_product', 'partial_sum', 'adjacent_difference', 'iota',
    'abs', 'labs', 'llabs', 'fabs', 'fma', 'pow', 'sqrt', 'cbrt', 'hypot', 'exp', 'exp2', 'expm1', 'log', 'log10', 'log1p', 'log2',
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
    'ceil', 'floor', 'trunc', 'round', 'lround', 'llround', 'nearbyint', 'rint', 'lrint', 'llrint',
    'fmod', 'remainder', 'remquo', 'copysign', 'nan', 'nanf', 'nanl', 'nextafter', 'nexttoward',
    'fdim', 'fmax', 'fmin', 'fpclassify', 'isfinite', 'isinf', 'isnan', 'isnormal', 'signbit', 'isgreater', 'isgreaterequal', 'isless', 'islessequal', 'islessgreater', 'isunordered',
    'bind', 'ref', 'cref', 'mem_fn', 'function', 'hash', 'placeholders', '_1', '_2', # ... placeholders
    'plus', 'minus', 'multiplies', 'divides', 'modulus', 'negate', 'equal_to', 'not_equal_to', 'greater', 'less', 'greater_equal', 'less_equal',
    'logical_and', 'logical_or', 'logical_not', 'bit_and', 'bit_or', 'bit_xor', 'bit_not',
    # Exceptions & Diagnostics
    'exception', 'bad_exception', 'nested_exception', 'throw_with_nested', 'rethrow_if_nested',
    'logic_error', 'domain_error', 'invalid_argument', 'length_error', 'out_of_range',
    'runtime_error', 'range_error', 'overflow_error', 'underflow_error',
    'system_error', 'error_code', 'error_condition', 'error_category',
    'bad_alloc', 'bad_cast', 'bad_typeid', 'bad_function_call',
    'assert', # cassert
    # Time & Date
    'chrono', 'duration', 'time_point', 'system_clock', 'steady_clock', 'high_resolution_clock',
    'duration_cast', 'time_point_cast', 'hours', 'minutes', 'seconds', 'milliseconds', 'microseconds', 'nanoseconds',
    'time_t', 'clock_t', 'tm', 'clock', 'time', 'difftime', 'mktime', 'strftime', 'strptime', 'localtime', 'gmtime', 'asctime', 'ctime',
    # Threading & Concurrency
    'thread', 'mutex', 'timed_mutex', 'recursive_mutex', 'recursive_timed_mutex',
    'lock_guard', 'unique_lock', 'shared_lock', # shared_lock is C++14, but often used
    'condition_variable', 'condition_variable_any', 'notify_all_at_thread_exit',
    'future', 'shared_future', 'promise', 'packaged_task', 'async', 'launch', 'future_status', 'future_error', 'future_errc',
    'atomic', 'atomic_flag', 'memory_order', 'memory_order_relaxed', 'memory_order_consume', 'memory_order_acquire', 'memory_order_release', 'memory_order_acq_rel', 'memory_order_seq_cst',
    'this_thread', 'get_id', 'yield', 'sleep_for', 'sleep_until',
    # Type Support & Traits
    'type_info', 'type_index', 'typeid', 'bad_cast', 'bad_typeid',
    'size_t', 'ptrdiff_t', 'nullptr_t', 'max_align_t', 'byte', # byte is C++17
    'integral_constant', 'bool_constant', 'true_type', 'false_type',
    'is_void', 'is_null_pointer', 'is_integral', 'is_floating_point', 'is_array', 'is_enum', 'is_union', 'is_class', 'is_function', 'is_pointer', 'is_lvalue_reference', 'is_rvalue_reference', 'is_member_object_pointer', 'is_member_function_pointer',
    'is_fundamental', 'is_arithmetic', 'is_scalar', 'is_object', 'is_compound', 'is_reference', 'is_member_pointer',
    'is_const', 'is_volatile', 'is_trivial', 'is_trivially_copyable', 'is_standard_layout', 'is_pod', 'is_literal_type', 'is_empty', 'is_polymorphic', 'is_abstract', 'is_final', 'is_aggregate',
    'is_signed', 'is_unsigned', 'is_bounded_array', 'is_unbounded_array',
    'is_constructible', 'is_trivially_constructible', 'is_nothrow_constructible', 'is_default_constructible', 'is_copy_constructible', 'is_move_constructible',
    'is_assignable', 'is_trivially_assignable', 'is_nothrow_assignable', 'is_copy_assignable', 'is_move_assignable',
    'is_destructible', 'is_trivially_destructible', 'is_nothrow_destructible',
    'is_swappable_with', 'is_swappable', 'is_nothrow_swappable_with', 'is_nothrow_swappable',
    'has_virtual_destructor',
    'alignment_of', 'rank', 'extent',
    'is_same', 'is_base_of', 'is_convertible',
    'remove_const', 'remove_volatile', 'remove_cv', 'add_const', 'add_volatile', 'add_cv',
    'remove_reference', 'add_lvalue_reference', 'add_rvalue_reference',
    'remove_pointer', 'add_pointer',
    'make_signed', 'make_unsigned',
    'remove_extent', 'remove_all_extents',
    'aligned_storage', 'aligned_union', 'decay', 'enable_if', 'conditional', 'common_type', 'underlying_type', 'result_of',
    # Random Number Generation
    'random', 'random_device', 'default_random_engine', 'minstd_rand0', 'minstd_rand', 'mt19937', 'mt19937_64', 'ranlux24_base', 'ranlux48_base', 'ranlux24', 'ranlux48', 'knuth_b',
    'uniform_int_distribution', 'uniform_real_distribution', 'bernoulli_distribution', 'binomial_distribution', 'geometric_distribution', 'negative_binomial_distribution',
    'poisson_distribution', 'exponential_distribution', 'gamma_distribution', 'weibull_distribution', 'extreme_value_distribution',
    'normal_distribution', 'lognormal_distribution', 'chi_squared_distribution', 'cauchy_distribution', 'fisher_f_distribution', 'student_t_distribution',
    'discrete_distribution', 'piecewise_constant_distribution', 'piecewise_linear_distribution', 'seed_seq', 'generate_canonical',
    # Other C++ related keywords/identifiers usually not replaced
    'std', 'nullptr',

    # 2. Common Predefined Macros & Compiler Macros
    'NULL', 'TRUE', 'FALSE', 'EOF', 'EXIT_SUCCESS', 'EXIT_FAILURE',
    'ASSERT', 'static_assert', # Note: static_assert is also a C++ keyword
    'DEBUG', '_DEBUG', 'NDEBUG',
    '__FILE__', '__LINE__', '__DATE__', '__TIME__', '__func__', '__FUNCTION__', '__PRETTY_FUNCTION__',
    '_WIN32', '_WIN64', '__linux__', '__APPLE__', '__MACH__', '__unix__', '__posix',
    '__GNUC__', '__clang__', '_MSC_VER', '__cplusplus',
    'offsetof', 'va_list', 'va_start', 'va_arg', 'va_end', 'va_copy',
    # --- 新增：明确排除常见的预处理相关词语，以防万一 ---
    'include', 'define', 'undef', 'ifdef', 'ifndef', 'if', 'elif', 'else', 'endif', 'line', 'error', 'pragma', 'defined',
    # C++17/C++20 Preprocessor Conditionals
    '__has_include', '__has_cpp_attribute',
    # Common #pragma arguments/keywords (Compiler-specific, but common usages)
    'once', 'pack', 'warning', 'message', 'push', 'pop', 'region', 'endregion', 'omp', # OpenMP often uses 'omp'

    # 3. Common C Standard Library Functions (Many overlap with C++ headers)
    # stdio.h
    'printf', 'fprintf', 'sprintf', 'snprintf', 'vprintf', 'vfprintf', 'vsprintf', 'vsnprintf',
    'scanf', 'fscanf', 'sscanf', 'vscanf', 'vfscanf', 'vsscanf',
    'fopen', 'freopen', 'fclose', 'fflush', 'setbuf', 'setvbuf',
    'fread', 'fwrite', 'fgetc', 'getc', 'getchar', 'fgets', 'fputc', 'putc', 'putchar', 'fputs', 'puts', 'ungetc',
    'fseek', 'ftell', 'rewind', 'fgetpos', 'fsetpos',
    'clearerr', 'feof', 'ferror', 'perror',
    'remove', 'rename', 'tmpfile', 'tmpnam',
    'stdin', 'stdout', 'stderr',
    # stdlib.h
    'malloc', 'calloc', 'realloc', 'free', 'aligned_alloc',
    'atoi', 'atof', 'atol', 'atoll', 'strtod', 'strtof', 'strtold', 'strtol', 'strtoul', 'strtoll', 'strtoull',
    'rand', 'srand', 'abort', 'atexit', 'exit', '_Exit', 'at_quick_exit', 'quick_exit', 'getenv', 'system', 'perror',
    'bsearch', 'qsort',
    # 'abs', 'labs', 'llabs' are also in <cmath>
    'div', 'ldiv', 'lldiv',
    'mblen', 'mbtowc', 'wctomb', 'mbstowcs', 'wcstombs',
    # string.h (cstring)
    'strcpy', 'strncpy', 'strcat', 'strncat', 'strcmp', 'strncmp', 'strcoll', 'strxfrm',
    'strchr', 'strrchr', 'strspn', 'strcspn', 'strpbrk', 'strstr', 'strtok', 'strerror',
    'memset', 'memcpy', 'memmove', 'memcmp', 'memchr',
    'strlen',
    # time.h (ctime)
    # 'clock_t', 'time_t', 'tm' are types
    # 'clock', 'time', 'difftime', 'mktime', 'strftime', 'localtime', 'gmtime', 'asctime', 'ctime' listed above
    # locale.h (clocale)
    'setlocale', 'localeconv',
    # setjmp.h (csetjmp)
    'setjmp', 'longjmp', 'jmp_buf',
    # signal.h (csignal)
    'signal', 'raise', 'SIG_DFL', 'SIG_ERR', 'SIG_IGN', 'SIGABRT', 'SIGFPE', 'SIGILL', 'SIGINT', 'SIGSEGV', 'SIGTERM',

    # 4. Common POSIX / Linux Identifiers (Not exhaustive)
    # Types
    'pid_t', 'uid_t', 'gid_t', 'off_t', 'mode_t', 'ssize_t', 'pthread_t', 'pthread_attr_t', 'ifreq',
    'pthread_mutex_t', 'pthread_mutexattr_t', 'pthread_cond_t', 'pthread_condattr_t', 'pthread_rwlock_t', 'pthread_rwlockattr_t',
    'pthread_key_t', 'sem_t', 'mqd_t', 'DIR', 'dirent', 'stat', 'statfs', 'sigset_t', 'siginfo_t', 'stack_t', 'termios', 'canid_t',
    'timespec', 'timeval', 'timezone', 'fd_set', 'sockaddr', 'sockaddr_storage', 'sockaddr_in', 'sockaddr_in6', 'sockaddr_un', 'sockaddr_can', 'socklen_t', 'sa_family_t', 'addrinfo', 'can_frame', 'can_filter', 'linger', 'sysinfo',
    # Constants
    'AF_INET', 'AF_INET6', 'AF_UNIX', 'AF_CAN', 'AF_UNSPEC', 'PF_CAN', 'SOCK_STREAM', 'SOCK_DGRAM', 'SOCK_RAW', 'SOCK_SEQPACKET', 'CAN_RAW',
    'SOL_SOCKET', 'SOL_TCP', 'SOL_CAN_RAW', 'SO_REUSEADDR', 'SO_KEEPALIVE', 'SO_ERROR', 'SO_SNDBUF', 'SO_RCVBUF', 'SO_SNDTIMEO', 'SO_RCVTIMEO', 'SO_LINGER', 'SO_BSDCOMPAT', 'TCP_NODELAY', 'TCP_KEEPIDLE', 'TCP_KEEPINTVL', 'TCP_KEEPCNT', 'CAN_RAW_FILTER',
    'IPPROTO_IP', 'IPPROTO_TCP', 'IPPROTO_UDP', 'IPPROTO_ICMP', 'IPPROTO_RAW',
    'O_RDONLY', 'O_WRONLY', 'O_RDWR', 'O_CREAT', 'O_EXCL', 'O_TRUNC', 'O_APPEND', 'O_NONBLOCK', 'O_NOCTTY', 'O_SYNC', 'O_ASYNC',
    'F_OK', 'R_OK', 'W_OK', 'X_OK', 'SEEK_SET', 'SEEK_CUR', 'SEEK_END',
    'STDIN_FILENO', 'STDOUT_FILENO', 'STDERR_FILENO',
    'S_IFMT', 'S_IFSOCK', 'S_IFLNK', 'S_IFREG', 'S_IFBLK', 'S_IFDIR', 'S_IFCHR', 'S_IFIFO', 'S_ISUID', 'S_ISGID', 'S_ISVTX',
    'S_IRWXU', 'S_IRUSR', 'S_IWUSR', 'S_IXUSR', 'S_IRWXG', 'S_IRGRP', 'S_IWGRP', 'S_IXGRP', 'S_IRWXO', 'S_IROTH', 'S_IWOTH', 'S_IXOTH',
    'FD_SETSIZE', 'FD_ZERO', 'FD_SET', 'FD_CLR', 'FD_ISSET',
    'PTHREAD_MUTEX_INITIALIZER', 'PTHREAD_COND_INITIALIZER', 'PTHREAD_RWLOCK_INITIALIZER',
    'SIG_BLOCK', 'SIG_UNBLOCK', 'SIG_SETMASK',
    'INADDR_ANY', 'MSG_NOSIGNAL', 'IPC_CREAT',
    'EAGAIN', 'EWOULDBLOCK', 'EINPROGRESS', 'EINTR',
    # termios.h constants (baud rates, flags)
    'B0', 'B50', 'B75', 'B110', 'B134', 'B150', 'B200', 'B300', 'B600', 'B1200', 'B1800', 'B2400', 'B4800', 'B9600', 'B19200', 'B38400', 'B57600', 'B115200', 'B230400', 'B460800',
    'ICANON', 'ECHO', 'ECHOE', 'ECHOK', 'ECHONL', 'ISIG', 'IEXTEN', 'NOFLSH', 'TOSTOP', 'PENDIN',
    'IGNBRK', 'BRKINT', 'IGNPAR', 'PARMRK', 'INPCK', 'ISTRIP', 'INLCR', 'IGNCR', 'ICRNL', 'IUCLC', 'IXON', 'IXOFF', 'IXANY', 'IMAXBEL', 'IUTF8',
    'OPOST', 'OLCUC', 'ONLCR', 'OCRNL', 'ONOCR', 'ONLRET', 'OFILL', 'OFDEL', 'NLDLY', 'NL0', 'NL1', 'CRDLY', 'CR0', 'CR1', 'CR2', 'CR3', 'TABDLY', 'TAB0', 'TAB1', 'TAB2', 'TAB3', 'BSDLY', 'BS0', 'BS1', 'VTDLY', 'VT0', 'VT1', 'FFDLY', 'FF0', 'FF1',
    'CSIZE', 'CS5', 'CS6', 'CS7', 'CS8', 'CSTOPB', 'CREAD', 'PARENB', 'PARODD', 'HUPCL', 'CLOCAL', 'CMSPAR', 'CRTSCTS',
    'VINTR', 'VQUIT', 'VERASE', 'VKILL', 'VEOF', 'VTIME', 'VMIN', 'VSWTC', 'VSTART', 'VSTOP', 'VSUSP', 'VEOL', 'VREPRINT', 'VDISCARD', 'VWERASE', 'VLNEXT', 'VEOL2', 'NCCS',
    'TCSANOW', 'TCSADRAIN', 'TCSAFLUSH', 'TCIFLUSH', 'TCOFLUSH', 'TCIOFLUSH', 'TCIOFF', 'TCION', 'TCOOFF', 'TCOON',
    'F_GETFL', 'F_SETFL', 'PR_GET_NAME', 'PR_SET_NAME',
    'SIOCGIFINDEX', 'TIOCGSERIAL', 'TIOCSSERIAL', 'TIOCGRS485', 'TIOCSRS485', 'WDIOC_SETTIMEOUT', 'WDIOC_KEEPALIVE',
    # Functions
    'read', 'write', 'pread', 'pwrite', 'pipe', 'pipe2', 'alarm', 'sleep', 'usleep', 'pause',
    'chown', 'fchown', 'lchown', 'chdir', 'fchdir', 'getcwd', 'dup', 'dup2', 'dup3',
    'access', 'faccessat', 'execve', 'execl', 'execlp', 'execle', 'execv', 'execvp', '_exit', 'exit',
    'fork', 'vfork', 'getpid', 'getppid', 'getuid', 'geteuid', 'getgid', 'getegid',
    'setuid', 'seteuid', 'setgid', 'setegid', 'getpgid', 'setpgid', 'getpgrp', 'setpgrp',
    'getsid', 'setsid', 'gethostname', 'sethostname', 'getlogin', 'getlogin_r', 'ttyname', 'ttyname_r', 'isatty',
    'link', 'linkat', 'symlink', 'symlinkat', 'readlink', 'readlinkat', 'unlink', 'unlinkat', 'rmdir',
    'sync', 'fsync', 'fdatasync', 'truncate', 'ftruncate',
    'open', 'openat', 'creat', 'fcntl', 'ioctl',
    'opendir', 'fdopendir', 'readdir', 'readdir_r', 'closedir', 'rewinddir', 'seekdir', 'telldir',
    'chmod', 'fchmod', 'fchmodat', 'umask', 'mkdir', 'mkdirat', 'mknod', 'mknodat',
    'statfs', 'fstatfs',
    'wait', 'waitpid', 'waitid',
    'socket', 'socketpair', 'bind', 'connect', 'listen', 'accept', 'accept4', 'shutdown', 'close',
    'send', 'sendto', 'sendmsg', 'recv', 'recvfrom', 'recvmsg',
    'getsockname', 'getpeername', 'getsockopt', 'setsockopt',
    'getaddrinfo', 'freeaddrinfo', 'gai_strerror', 'getnameinfo',
    'tcgetattr', 'tcsetattr', 'cfsetispeed', 'cfsetospeed', 'cfgetispeed', 'cfgetospeed', 'tcsendbreak', 'tcdrain', 'tcflush', 'tcflow', 'cfmakeraw',
    'htons', 'htonl', 'ntohs', 'ntohl', 'inet_addr', 'inet_aton', 'inet_ntoa', 'inet_ntop', 'inet_pton', 'sysinfo', 'syscall', 'pthread_sigmask', 'kill',
    'select', 'pselect', 'poll', 'ppoll', 'epoll_create', 'epoll_create1', 'epoll_ctl', 'epoll_wait', 'epoll_pwait',
    'pthread_create', 'pthread_join', 'pthread_detach', 'pthread_exit', 'pthread_self', 'pthread_equal', 'pthread_cancel', 'pthread_setcancelstate', 'pthread_setcanceltype', 'pthread_testcancel',
    'pthread_attr_init', 'pthread_attr_destroy', 'pthread_attr_setdetachstate', 'pthread_attr_getdetachstate', 'pthread_attr_setschedparam', 'pthread_attr_getschedparam', 'pthread_attr_setschedpolicy', 'pthread_attr_getschedpolicy', 'pthread_attr_setinheritsched', 'pthread_attr_getinheritsched', 'pthread_attr_setscope', 'pthread_attr_getscope', 'pthread_attr_setstacksize', 'pthread_attr_getstacksize', 'pthread_attr_setstack', 'pthread_attr_getstack',
    'pthread_mutex_init', 'pthread_mutex_destroy', 'pthread_mutex_lock', 'pthread_mutex_trylock', 'pthread_mutex_unlock', 'pthread_mutex_timedlock',
    'pthread_cond_init', 'pthread_cond_destroy', 'pthread_cond_wait', 'pthread_cond_timedwait', 'pthread_cond_signal', 'pthread_cond_broadcast',
    'pthread_rwlock_init', 'pthread_rwlock_destroy', 'pthread_rwlock_rdlock', 'pthread_rwlock_tryrdlock', 'pthread_rwlock_wrlock', 'pthread_rwlock_trywrlock', 'pthread_rwlock_unlock', 'pthread_rwlock_timedrdlock', 'pthread_rwlock_timedwrlock',
    'pthread_key_create', 'pthread_key_delete', 'pthread_setspecific', 'pthread_getspecific',
    'pthread_once', 'pthread_atfork',
    'sigaction', 'sigprocmask', 'sigpending', 'sigsuspend', 'sigwait', 'sigwaitinfo', 'sigtimedwait', 'kill', 'killpg', 'raise', 'alarm', 'pause',
    'sigemptyset', 'sigfillset', 'sigaddset', 'sigdelset', 'sigismember',
    'sem_open', 'sem_close', 'sem_unlink', 'sem_wait', 'sem_trywait', 'sem_timedwait', 'sem_post', 'sem_getvalue', 'sem_init', 'sem_destroy',
    'dlopen', 'dlsym', 'dlclose', 'dlerror', # Dynamic linking
    'mmap', 'munmap', 'msync', 'mprotect', 'mlock', 'munlock', 'mlockall', 'munlockall', # Memory management
    'gettimeofday', 'settimeofday', 'clock_gettime', 'clock_settime', 'clock_getres', 'nanosleep', # Time
    'syslog', 'openlog', 'closelog', 'setlogmask', # Logging

    # 5. Common Windows API Identifiers (More examples, still not exhaustive)
    # Basic Types & Macros
    'BOOL', 'BYTE', 'WORD', 'DWORD', 'UINT', 'INT', 'LONG', 'ULONG', 'SHORT', 'USHORT', 'CHAR', 'WCHAR', 'TCHAR',
    'HANDLE', 'HWND', 'HINSTANCE', 'HMODULE', 'HDC', 'HICON', 'HCURSOR', 'HBRUSH', 'HMENU', 'HKEY', 'HRGN', 'HPEN', 'HFONT',
    'LPARAM', 'WPARAM', 'LRESULT', 'COLORREF',
    'LPSTR', 'LPCSTR', 'LPWSTR', 'LPCWSTR', 'LPTSTR', 'LPCTSTR', 'LPVOID', 'LPCVOID', 'DWORD_PTR', 'ULONG_PTR', 'LONG_PTR',
    'WINAPI', 'APIENTRY', 'CALLBACK', 'NTAPI',
    'TRUE', 'FALSE', 'NULL', 'INVALID_HANDLE_VALUE', 'MAX_PATH',
    'MAKEINTRESOURCE', 'LOWORD', 'HIWORD', 'LOBYTE', 'HIBYTE',
    # Core Functions
    'GetLastError', 'SetLastError', 'FormatMessageA', 'FormatMessageW', 'GetVersionExA', 'GetVersionExW', 'IsWindowsXPorGreater', 'IsWindowsVistaOrGreater', 'IsWindows7OrGreater', 'IsWindows8OrGreater', 'IsWindows10OrGreater',
    # File I/O & System Info
    'CreateFileA', 'CreateFileW', 'ReadFile', 'WriteFile', 'SetFilePointer', 'SetEndOfFile', 'GetFileSize', 'GetFileSizeEx', 'CloseHandle',
    'GetSystemDirectoryA', 'GetSystemDirectoryW', 'GetWindowsDirectoryA', 'GetWindowsDirectoryW', 'GetCurrentDirectoryA', 'GetCurrentDirectoryW', 'SetCurrentDirectoryA', 'SetCurrentDirectoryW',
    'GetFullPathNameA', 'GetFullPathNameW', 'GetTempPathA', 'GetTempPathW', 'CreateDirectoryA', 'CreateDirectoryW', 'RemoveDirectoryA', 'RemoveDirectoryW',
    'DeleteFileA', 'DeleteFileW', 'MoveFileA', 'MoveFileW', 'MoveFileExA', 'MoveFileExW', 'CopyFileA', 'CopyFileW', 'CopyFileExA', 'CopyFileExW',
    'FindFirstFileA', 'FindFirstFileW', 'FindNextFileA', 'FindNextFileW', 'FindClose', 'GetFileAttributesA', 'GetFileAttributesW', 'GetFileAttributesExA', 'GetFileAttributesExW',
    'GetSystemTime', 'GetLocalTime', 'SetSystemTime', 'SetLocalTime', 'GetTickCount', 'GetTickCount64', 'QueryPerformanceCounter', 'QueryPerformanceFrequency',
    # Process & Thread
    'GetCurrentProcess', 'GetCurrentProcessId', 'GetCurrentThread', 'GetCurrentThreadId',
    'CreateProcessA', 'CreateProcessW', 'TerminateProcess', 'ExitProcess', 'GetExitCodeProcess',
    'CreateThread', 'ExitThread', 'GetExitCodeThread', 'SuspendThread', 'ResumeThread', 'Sleep', 'SwitchToThread',
    'WaitForSingleObject', 'WaitForMultipleObjects', 'CreateEventA', 'CreateEventW', 'SetEvent', 'ResetEvent', 'PulseEvent',
    'CreateMutexA', 'CreateMutexW', 'ReleaseMutex', 'CreateSemaphoreA', 'CreateSemaphoreW', 'ReleaseSemaphore',
    'InitializeCriticalSection', 'EnterCriticalSection', 'LeaveCriticalSection', 'DeleteCriticalSection', 'TryEnterCriticalSection',
    'TlsAlloc', 'TlsFree', 'TlsSetValue', 'TlsGetValue',
    # Memory Management
    'VirtualAlloc', 'VirtualFree', 'VirtualProtect', 'VirtualQuery',
    'HeapCreate', 'HeapDestroy', 'HeapAlloc', 'HeapReAlloc', 'HeapFree', 'GetProcessHeap',
    'GlobalAlloc', 'GlobalFree', 'GlobalLock', 'GlobalUnlock',
    'LocalAlloc', 'LocalFree', 'LocalLock', 'LocalUnlock',
    # Dynamic Linking
    'LoadLibraryA', 'LoadLibraryW', 'LoadLibraryExA', 'LoadLibraryExW', 'FreeLibrary', 'GetProcAddress', 'GetModuleHandleA', 'GetModuleHandleW', 'GetModuleFileNameA', 'GetModuleFileNameW',
    # Windowing (User32.dll)
    'RegisterClassA', 'RegisterClassW', 'RegisterClassExA', 'RegisterClassExW', 'UnregisterClassA', 'UnregisterClassW',
    'CreateWindowExA', 'CreateWindowExW', 'DestroyWindow', 'ShowWindow', 'UpdateWindow', 'IsWindowVisible', 'IsWindowEnabled',
    'GetMessageA', 'GetMessageW', 'TranslateMessage', 'DispatchMessageA', 'DispatchMessageW', 'PeekMessageA', 'PeekMessageW',
    'PostMessageA', 'PostMessageW', 'SendMessageA', 'SendMessageW', 'PostThreadMessageA', 'PostThreadMessageW', 'SendNotifyMessageA', 'SendNotifyMessageW',
    'DefWindowProcA', 'DefWindowProcW', 'CallWindowProcA', 'CallWindowProcW', 'GetWindowLongA', 'GetWindowLongW', 'SetWindowLongA', 'SetWindowLongW', 'GetWindowLongPtrA', 'GetWindowLongPtrW', 'SetWindowLongPtrA', 'SetWindowLongPtrW',
    'GetClientRect', 'GetWindowRect', 'MoveWindow', 'SetWindowPos', 'BeginPaint', 'EndPaint', 'GetDC', 'ReleaseDC', 'InvalidateRect', 'ValidateRect',
    'MessageBoxA', 'MessageBoxW', 'MessageBoxExA', 'MessageBoxExW', 'DialogBoxParamA', 'DialogBoxParamW', 'EndDialog', 'GetDlgItem', 'SendDlgItemMessageA', 'SendDlgItemMessageW',
    'SetTimer', 'KillTimer', 'GetCursorPos', 'SetCursorPos', 'ScreenToClient', 'ClientToScreen',
    # GDI (Gdi32.dll)
    'CreateCompatibleDC', 'DeleteDC', 'CreateCompatibleBitmap', 'DeleteObject', 'SelectObject', 'GetStockObject',
    'CreatePen', 'CreateSolidBrush', 'CreateFontA', 'CreateFontW', 'SetTextColor', 'SetBkColor', 'SetBkMode',
    'TextOutA', 'TextOutW', 'DrawTextA', 'DrawTextW', 'Rectangle', 'Ellipse', 'MoveToEx', 'LineTo', 'BitBlt', 'StretchBlt',
    # Sockets (Winsock2.h - ws2_32.dll)
    'WSAStartup', 'WSACleanup', 'WSAGetLastError', 'socket', 'closesocket', 'bind', 'listen', 'accept', 'connect', 'send', 'recv', 'sendto', 'recvfrom',
    'select', 'ioctlsocket', 'gethostbyname', 'gethostbyaddr', 'getaddrinfo', 'freeaddrinfo', 'getnameinfo',
    # 'htons', 'htonl', 'ntohs', 'ntohl', 'inet_addr', 'inet_ntoa' are common but defined elsewhere too
    # Registry (Advapi32.dll)
    'RegOpenKeyExA', 'RegOpenKeyExW', 'RegCloseKey', 'RegQueryValueExA', 'RegQueryValueExW', 'RegSetValueExA', 'RegSetValueExW', 'RegCreateKeyExA', 'RegCreateKeyExW', 'RegDeleteKeyA', 'RegDeleteKeyW', 'RegDeleteValueA', 'RegDeleteValueW',

    # 6. Other Common Non-Replaceable Identifiers
    'main', 'wmain', '_tmain',
    'WinMain', 'wWinMain', '_tWinMain',
    'DllMain', '_DllMainCRTStartup',
    'argc', 'argv', 'envp', 'wargv', 'targv',
    'std', # Explicitly ensure std namespace itself is here

    # 7. Common Typedefs (Often project-specific or from C headers)
    # Fixed-width integers (from <cstdint> or similar)
    'int8_t', 'uint8_t', 'int16_t', 'uint16_t', 'int32_t', 'uint32_t', 'int64_t', 'uint64_t',
    'int_fast8_t', 'uint_fast8_t', 'int_fast16_t', 'uint_fast16_t', 'int_fast32_t', 'uint_fast32_t', 'int_fast64_t', 'uint_fast64_t',
    'int_least8_t', 'uint_least8_t', 'int_least16_t', 'uint_least16_t', 'int_least32_t', 'uint_least32_t', 'int_least64_t', 'uint_least64_t',
    'intmax_t', 'uintmax_t', 'intptr_t', 'uintptr_t', # Already listed but good to group
    # Custom types found in std_def.h
    'uint8', 'uint16', 'uint32', 'uint64',
    'int8', 'int16', 'int32', 'int64',
    'EBool', 'TId', 'THandle', 'EWeekDay', 'EErrorCode',
    # Other potentially common typedefs
    'byte', 'word', 'dword', 'qword', # Often used, overlaps with Windows types
    'bool8', 'bool16', 'bool32',
    'float32', 'float64',

    # 8. Specific Frameworks (Add as needed)
    # Example: Qt
    # 'QObject', 'QString', 'QWidget', 'QApplication', 'QMainWindow', 'QPushButton', 'QLabel', 'QLineEdit', 'QDialog', 'QList', 'QVector', 'QMap', 'SLOT', 'SIGNAL', 'emit',
    # Example: Boost
    # 'boost', 'shared_ptr', 'scoped_ptr', 'filesystem', 'thread', 'asio',

    # 9. Project Common Macros & Types (from analyzed headers)
    # from comMacro.h & traverse__VA_ARGS__mocro.h
    'LINE_SEPARATOR', 'ARRAY_LEN', 'VALID_ARRAY_INDEX', 'FOR_LOOP_ARRAY', 'VAR_MEM_ARGS', 'VAR_MEM_ARGS_CONST',
    'VAR_MEM_ARGS_CHAR', 'VAR_MEM_ARGS_CONST_CHAR', 'ARRAY_MEM_ARGS', 'ARRAY_MEM_ARGS_CONST', 'RESET_VAR',
    'RESET_PTR_VAR', 'RESET_MEM', 'MEMSET', 'MEMSET2ARR', 'MEMCPY', 'MEMCPY2ARR', 'MEMMOVE', 'MEMMOVE2ARR',
    'MEMCMP', 'MEMCMP_OF_ARR', 'STRNCPY', 'STRCPY2ARR', 'STRCPY_FROM_ARR', 'STRCAT', 'STRNCAT', 'STRNCMP',
    'STRNCMP_OF_ARR', 'STRPRI2ARR', 'STRLEN', 'STRLEN_OF_ARR', 'CLEAR_STR', 'IS_NULL_STR', 'IS_NOT_NULL_STR',
    'IS_VALID_HANDLE', 'NUM_OF_BITS', 'BYTE_OF_VAR', 'BITS_OF_VAR', 'BIT_VALUE_ADDR', 'BIT_VALUE', 'BIT_SET_1',
    'SET_BIT', 'CLEAR_BIT', 'LIMIT_MIN', 'LIMIT_MAX', 'MIN', 'MAX', 'CAST_OPERATE', 'CAST_ASSIGN', 'BIN_ASSIGN',
    'DEFINE_VAR_INIT', 'DEFINE_VAR_INIT_FROM_ADDR', 'TYPE_VALUE_OF_ADDR', 'READ_VAR_FROM_ADDR', 'READ_VAR_FROM_ADD_SELF_ADDR',
    'WRITE_VAR_TO_ADDR', 'WRITE_VAR_TO_ADD_SELF_ADDR', 'NAMESPACE_BEGIN', 'NAMESPACE_END', 'SWAP_VALUE', 'TO_BCD',
    'FROM_BCD', 'GET_MEMBER_SIZE', 'GET_MEMBER_TYPE', 'GET_MEMBER_ARRAY_LEN', 'offset_of', 'OFFSET_TO_END_OF_MEMBER',
    'FRONT_SIZE_OF_MEMBER', 'container_of', 'typecheck', 'CHAR_2_NUM', 'NUM_2_CHAR', 'IS_NUM', 'IS_LETTER', 'RND',
    'UP_CASE', 'LOWER_CASE', 'INC_SAT', 'B_CMD_TO_A_CMD', 'BA_CMD_TO_A_CMD', 'CASE_A_RETURN_B',
    'CASE_OTHER_NAME_2_OWN_NAME', 'CASE_OWN_NAME_2_OTHER_NAME', 'CASE_ENUM_2_TEXT_RETURN', 'CASE_ENUM_RETURN_STR',
    'SConstFactorial', 'SConstPow', 'CONST_FACTORIAL', 'CONST_POW', 'GET_VIRTUAL_FUNC_ADDR', '__LRY_tmp', '__dummy', '__dummy2',
    'PP_NARG', 'PP_NARG_', 'PP_ARG_N', 'PP_RSEQ_N', 'MANY', 'ONE', 'ZERO', 'CHECK_MACRO_PARAMS_COUNT',
    'CHECK_MACRO_PARAMS_COUNT_', 'CHECK_PARAMS_COUNT_ARG_N', 'CHECK_PARAMS_COUNT_RSEQ_N', 'STR', 'STR1', 'STR2',
    'CONNECT_2_ARGS2', 'CONNECT_2_ARGS1', 'CONNECT_2_ARGS', 'REMOVE_BRACKETS1', 'REMOVE_BRACKETS',
    '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8', '_9', '_10', '_11', '_12', '_13', '_14', '_15', '_16', '_17', '_18', '_19', '_20',
    '_21', '_22', '_23', '_24', '_25', '_26', '_27', '_28', '_29', '_30', '_31', '_32', '_33', '_34', '_35', '_36', '_37', '_38', '_39', '_40',
    '_41', '_42', '_43', '_44', '_45', '_46', '_47', '_48', '_49', '_50', '_51', '_52', '_53', '_54', '_55', '_56', '_57', '_58', '_59', '_60',
    '_61', '_62', '_63', 'N', # Added placeholders from PP_ARG_N macro example
    'FOR_EACH_1', 'FOR_EACH_2', 'FOR_EACH_3', 'FOR_EACH_4', 'FOR_EACH_5', 'FOR_EACH_6', 'FOR_EACH_7', 'FOR_EACH_8',
    'FOR_EACH_9', 'FOR_EACH_10', 'FOR_EACH_11', 'FOR_EACH_12', 'FOR_EACH_13', 'FOR_EACH_14', 'FOR_EACH_15', 'FOR_EACH_16',
    'FOR_EACH_', 'FOR_EACH', 'what', 'paramInfo', 'connectInfo',
    # from headerComMacro.h
    'Q_DISABLE_COPY', 'Q_DECLARE_PRIVATE', 'Q_DECLARE_PRIVATE_D', 'Q_DECLARE_PUBLIC', 'Q_D', 'Q_Q',
    'SINGLETON', 'SINGLETON_C_D', 'qGetPtrHelper',
    # from simpleComMacro - 简化版.h
    'SAVE_DEBUG_LOG', 'SAVE_INFO_LOG', 'SAVE_ERROR_LOG', 'YES', 'NO',
    # from std_def.h (Macros, Enums, Structs, Unions, Members)
    'SI_DEFINED_UINT8', 'SI_DEFINED_UINT16', 'SI_DEFINED_UINT32', 'SI_DEFINED_INT8', 'SI_DEFINED_INT16',
    'SI_DEFINED_INT32', 'SI_DEFINED_UINT64', 'SI_DEFINED_INT64', 'SI_INVALID_ID', 'SI_INVALID_CODE',
    'SI_INVALID_INDEX', 'SI_INVALID_HANDLE', 'SI_INVALID_ADDRESS', 'SPECIALIZED_ERROR_CODE_BASE_VALUE',
    'BMS_ERROR_CODE_BASE_VALUE', 'EWeekDay', 'EErrorCode',
    'SI_MONDAY', 'SI_TUESDAY', 'SI_WEDNESDAY', 'SI_THURSDAY', 'SI_FRIDAY', 'SI_SATURDAY', 'SI_SUNDAY',
    'ERROR_SUCCESS', 'ERROR_FAIL', 'ERROR_USER_NOT_FOUND', 'ERROR_PASSWD_ERROR', 'ERROR_PERMISSION_DENIED',
    'ERROR_DATA_FORMAT_ERROR', 'ERROR_FUNCTION_NOT_SUPPORTED', 'ERROR_HEAD_FORMAT_ERROR', 'ERROR_CHECK_CODE_FAIL',
    'ERROR_PACK_SIZE_TOO_BIG', 'ERROR_PACK_CMD_UNKNOWN', 'ERROR_BAD_PARAMETER', 'ERROR_SERVER_NOT_RESPONSE',
    'ERROR_SERVER_NOT_REPLY', 'ERROR_TERM_NOT_RESPONSE', 'ERROR_TERM_NOT_REPLY', 'ERROR_DATA_BASE_ERROR',
    'ERROR_NO_MEMORY', 'ERROR_ALREADY_INITIALIZED', 'ERROR_INVALID_DESCRIPTOR', 'ERROR_SYSCALL_FAIL',
    'ERROR_CREATE_THREAD_FAIL', 'ERROR_SET_THREAD_DETACH_FAIL', 'ERROR_RECV_DATA_TIMEOUT', 'ERROR_TAIL_FORMAT_ERROR',
    'ERROR_SEND_DATA_FAIL', 'ERROR_CREATE_FILE_FAIL', 'ERROR_DEL_FILE_FAIL', 'ERROR_OPEN_FILE_FAIL',
    'ERROR_CLOSE_FILE_FAIL', 'ERROR_READ_FILE_FAIL', 'ERROR_WRITE_FILE_FAIL', 'ERROR_QUEUE_FULL',
    'ERROR_QUEUE_EMPTY', 'ERROR_QUEUE_BUSY', 'ERROR_LOGIN_PASSWD_ERROR', 'ERROR_NO_ENOUGH_SPARE_BUF',
    'ERROR_THIRD_CALL_FAIL', 'ERROR_NET_DISCONNECTED', 'ERROR_READ_IO_FAIL', 'ERROR_WRITE_IO_FAIL',
    'ERROR_READ_PUBLIC_DATA_FAIL', 'ERROR_WRITE_PUBLIC_DATA_FAIL', 'ERROR_INVALID_OPERATION',
    'ERROR_DATA_FIELD_SIZE_INCORRECT', 'ERROR_SIGNAL_REGISTRATION_FULL', 'ERROR_SIGNAL_SLOT_ALREADY_CONNECTED',
    'ERROR_SIGNAL_SLOT_CONNECTION_POOL_FULL', 'ERROR_NO_SUCH_SIGNAL_SLOT_CONNECTION', 'ERROR_FILE_NAME_SIZE_BEYOND_LIMIT',
    'ERROR_SAVE_RECORD_FAIL', 'ERROR_RESOURCES_BUSY', 'ERROR_GET_PTR_HANDLE_FAIL', 'ERROR_RECV_DATA_FAIL',
    'ERROR_PACK_CMD_ALREADY_REGISTERED', 'ERROR_PACK_CMD_UNREGISTERED', 'ERROR_ALREADY_REGISTERED',
    'ERROR_UNREGISTERED_FAIL', 'ERROR_LOGIN_FAIL', 'ERROR_SET_SYSTEM_TIME_FAIL', 'ERROR_NO_FREE_HANDLES',
    'ERROR_INVALID_HANDLE', 'ERROR_INVALID_ID', 'ERROR_TIMEOUT', 'ERROR_DEVICE_BUSY', 'ERROR_NO_INIT',
    'ERROR_BEYOND_MAX_COUNT', 'ERROR_BEYOND_MIN_COUNT', 'ERROR_LOCK_FAIL', 'ERROR_UNLOCK_FAIL',
    'ERROR_STATE_ERROR', 'ERROR_NULL_POINTER', 'ERROR_BAD_PARAM_NULL_PTR', 'ERROR_FUNC_RETURN_NULL_PTR',
    'ERROR_COUNT_ERROR', 'ERROR_NO_ENOUGH_MONEY', 'ERROR_REPETITIVE_OPERATION', 'ERROR_PARAMETER_NOT_COMPLETE',
    'ERROR_LENGTH_INCORRECT', 'ERROR_DEVICE_NOT_AVAILABLE', 'ERROR_TASK_BEING_PERFORMED', 'ERROR_NOT_FOUND',
    'ERROR_OPERA_FILE_FAIL', 'ERROR_TYPE_INCORRECT', 'ERROR_OPEN_DEVICE_FAIL', 'ERROR_ALREADY_STARTED',
    'ERROR_ALREADY_STOPPED', 'ERROR_PEER_ADDR_INCORRECT', 'ERROR_GET_FAIL', 'ERROR_SET_FAIL', 'ERROR_PEER_EXEC_FAIL',
    'ERROR_CHECK_FAIL', 'ERROR_ADDRESS_ERROR', 'ERROR_SWITCH_UNKNOWN_CASE', 'ERROR_RETRY_LATER',
    'ERROR_OPERATION_NOT_ALLOWED', 'ERROR_FINAL_FAIL', 'ERROR_DEVICE_NOT_FOUND', 'ERROR_DYNAMIC_CAST_ERROR',
    'ERROR_UNKNOWN_ERROR', 'ERROR_SYSTEM_FAULT', 'ERROR_CAN_SEND_DATA_FAIL', 'ERROR_HAS_BEEN_IN_CHARGE',
    'ERROR_CHARGER_IN_PAUSE_MODE', 'ERROR_CC1_DISCONNECTED', 'ERROR_INSULATION_DETECTION_START_FAIL',
    'ERROR_INSULATION_DETECTION_TIMEOUT', 'ERROR_INSULATION_DETECTION_ABNORMAL', 'ERROR_BMS_AUXILIARY_POWER_ABNORMAL',
    'ERROR_BMS_AUXILIARY_POWER_NOT_MATCH', 'ERROR_BMS_AUXILIARY_POWER_START_FAIL', 'ERROR_START_CHARGING_TIMEOUT',
    'ERROR_WAIT_BMS_BRM_TIMEOUT', 'ERROR_WAIT_BMS_BCP_TIMEOUT', 'ERROR_WAIT_BMS_BRO_TIMEOUT',
    'ERROR_WAIT_BMS_BCS_TIMEOUT', 'ERROR_WAIT_BMS_BCL_TIMEOUT', 'ERROR_WAIT_BMS_BST_TIMEOUT',
    'ERROR_WAIT_BMS_BSD_TIMEOUT', 'ERROR_HANDSHAKE_STAGE_TIMEOUT', 'ERROR_PARAM_CONFIG_STAGE_TIMEOUT',
    'ERROR_CHARGING_STAGE_TIMEOUT', 'ERROR_CHARGING_END_STAGE_TIMEOUT',
    'UInt32Bit', 'EventStruct', 'all', 'bit',
    # from log.h & simpleLog.h (Logging, Debugging, Error Handling Macros)
    'SIMPLE_PRINT', 'SIMPLE_LOG', 'MY_ASSERT', 'MY_DEBUG', 'MY_INFO', 'MY_ERROR', 'MY_SYSCALL_ERROR',
    'ASSERT_PRINT', 'DEBUG_PRINT', 'DEBUG_LOG', 'DEBUG_SAVE', 'DEBUG', 'INFO_PRINT', 'INFO_LOG', 'INFO_SAVE', 'INFO',
    'ERROR_PRINT', 'ERROR_LOG', 'ERROR_SAVE', 'ERROR', 'SYSCALL_ERROR_PRINT', 'SYSCALL_ERROR_LOG', 'SYSCALL_ERROR_SAVE', 'SYSCALL_ERROR',
    'CALLFUNC_ERROR', 'NONE', 'TYPE_INT', 'TYPE_UINT', 'TYPE_LONG_INT', 'TYPE_LONG_UINT', 'TYPE_FLOAT', 'TYPE_DBL', 'TYPE_CHR', 'TYPE_STR', 'TYPE_PTR', 'TYPE_HEX',
    'PRINT_ONE_TYPE_VARS', 'PRINT_ONE_TYPE_VARS_E', 'PRINT_ONE_TYPE_VARS_COMBINATION', 'PRINT_MANY_TYPE_VARS', 'PRINT_ONE_VAR', 'VAR_CONNECT_INFO',
    'PRINT_PTR', 'PRINT_INT', 'PRINT_STR', 'PRINT_DBL', 'PRINT_CHR', 'PRINT_HEX', 'PRINT_PTR_E', 'PRINT_INT_E', 'PRINT_STR_E', 'PRINT_DBL_E', 'PRINT_CHR_E', 'PRINT_HEX_E',
    'HERE_ENABLE', 'HERE', 'HERE_ERROR', 'HERE_ERROR_TEXT',
    'SYSCALL', 'SYSCALL2', 'SYSCALL_FAIL_RETURN_DFL', 'SYSCALL2_FAIL_RETURN_DFL', 'SYSCALL_FAIL_RETURN_SPEC', 'SYSCALL2_FAIL_RETURN_SPEC',
    'SYSCALL_FAIL_EXEC', 'SYSCALL2_FAIL_EXEC', 'SYSCALL_CHECK_SUCCVAL_RETURN_SPEC', 'SYSCALL_CHECK_FAILVAL_RETURN_SPEC', 'SYSCALL_CHECK_SUCCVAL_FAIL_EXEC',
    'SYSCALL_CHECK_FAILVAL_FAIL_EXEC', 'SYSCALL_CHECK_RETVAL_FAIL_EXEC',
    'CALLFUNC', 'CALLFUNC2', 'CALLFUNC_FAIL_RETURN', 'CALLFUNC2_FAIL_RETURN_DFL', 'CALLFUNC2_FAIL_RETURN_SPEC', 'CALLFUNC_FAIL_EXEC', 'CALLFUNC2_FAIL_EXEC',
    'CALLFUNC_CHECK_SUCCVAL_RETURN_SPEC', 'CALLFUNC_CHECK_FAILVAL_RETURN_SPEC', 'CALLFUNC_CHECK_SUCCVAL_FAIL_EXEC', 'CALLFUNC_CHECK_FAILVAL_FAIL_EXEC',
    'CALLFUNC_CHECK_RETVAL_FAIL_EXEC', 'CALLFUNC_CHECK_RETVAL2_FAIL_EXEC', 'CALLFUNC_FAIL_SPECVAL_EXEC', 'CALLFUNC2_FAIL_SPECVAL_EXEC',
    'CALLFUNC_CHECK_SUCCVAL_FAIL_SPECVAL_EXEC', 'CALLFUNC_CHECK_FAILVAL_FAIL_SPECVAL_EXEC',
    'MALLOC_MEM_FAIL_EXIT', 'MALLOC_MEM_FAIL_RETURN_DFL', 'MALLOC_MEM_FAIL_EXEC', 'MALLOC_DEBUG_ENABLE', 'FREE_DEBUG_ENABLE', 'MALLOC_DEBUG', 'FREE_DEBUG',
    'DELETE', 'DELETE_ARRAY', 'DELETE_RDONLY', 'DELETE_ARRAY_RDONLY',
    'LOCK_DEBUG_ENABLE', 'CALL_LOCK', 'CALL_UNLOCK',
    'CHECK_FAIL_EXEC', 'CHECK_FAIL_RETURN_SPEC', 'CHECK_FAIL_RETURN_DFL', 'PROCESS_ONE_COND', 'CHECK_MANY_COND', 'CHECK_ONE_COND',
    'SELECT_CHECK2', 'SELECT_CHECK1', 'SELECT_CHECK_MACRO', 'CHECK_PTR_FAIL_EXEC', 'CHECK_ONE_FAIL_EXEC', 'CHECK_MANY_FAIL_EXEC',
    'CHECK_VALUE_FAIL_EXEC', 'CHECK_INT_EQUAL_VALUE', 'CHECK_INT_EQUAL_VALUE_FAIL_EXEC', 'CHECK_INT_VALUE_FAIL_EXEC', 'CHECK_INT_VALUE_FAIL_RETURN_SPEC',
    'CHECK_INT_VALUE_FAIL_RETURN_DFL', 'CHECK_INT_VALUE', 'CHECK_ERROR_CODE_FAIL_RETURN', 'CHECK_ERROR_CODE_FAIL_EXEC', 'CHECK_VALUE_FAIL_RETURN_SPEC',
    'CHECK_VALUE_FAIL_RETURN_DFL', 'CHECK_VALUE',
    'WELCOME_INFO', 'PRINT_ARRAY_HEX_MEM', 'PRINT_DATA_HEX_MEM', 'PRINT_DATA_HEX', 'LOG_DATA_HEX', 'SAVE_DATA_HEX',
    'PRINT_REPORT_SEND_INFO', 'PRINT_REPORT_RECV_INFO', 'PRINT_RESPONSE_SEND_INFO', 'PRINT_RESPONSE_RECV_INFO',
    'SWITCH_DEFAULT_CASE_RETURN_DFL', 'SWITCH_DEFAULT_CASE_RETURN_SPEC', 'SWITCH_DEFAULT_CASE_EXEC',
    'SET_THREAD_NAME_PRINT', 'HERE_EMIT',
    'DEBUG_COLOR', 'INFO_COLOR', 'ERROR_COLOR', 'CLOSE_DEBUG_COLOR', 'CLOSE_INFO_COLOR', 'CLOSE_ERROR_COLOR',
    'DEBUG_LEVEL', 'INFO_LEVEL', 'ERROR_LEVEL', 'LOCATION_INFO', 'LOCATION_PARAM', 'SYSCALL_EXTRA_INFO', 'PRINT',
    '__pLog_LRY_temp', '__buf_LRY_temp', '__SYSCALL_temp_ret', '__ret_temp', '__check_count_temp',
}

def get_script_dir():
    """获取脚本所在目录的绝对路径"""
    if getattr(sys, 'frozen', False):  # 打包成exe的情况
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
    

def generate_fixed_mapping():
    """生成随机字母数字映射表并保存到文件"""
    # 包含所有大写字母、小写字母和数字
    chars = list(
        string.ascii_uppercase +  # A-Z (26)
        string.ascii_lowercase +  # a-z (26)
        string.digits             # 0-9 (10)
    )
    
    # 创建打乱后的目标字符列表
    shuffled = chars.copy()
    random.shuffle(shuffled)
    
    # 生成映射关系
    mapping = {orig: tgt for orig, tgt in zip(chars, shuffled)}
    return mapping, {v:k for k,v in mapping.items()}

def load_or_create_mapping():
    """从配置文件加载或创建新映射表"""
    MAPPING_CONFIG_PATH = os.path.join(get_script_dir(), 'mapping_config.json')

    if os.path.exists(MAPPING_CONFIG_PATH):
        try:
            with open(MAPPING_CONFIG_PATH, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
                if validate_mapping(mapping):
                    return mapping, {v:k for k,v in mapping.items()}
                else:
                    messagebox.showwarning("配置问题", "映射表校验失败，已创建新表")
        except Exception as e:
            messagebox.showwarning("配置错误", f"配置文件加载失败：{str(e)}\n已创建新映射表")
    else:
        # 首次运行时不显示警告
        pass
    
    # 创建新映射表
    mapping, reverse_mapping = generate_fixed_mapping()
    # MAPPING_CONFIG_PATH = os.path.join(get_script_dir(), 'mapping_config.json')
    save_reverse_mapping(mapping, MAPPING_CONFIG_PATH)
    return mapping, reverse_mapping

def validate_mapping(mapping):
    """验证映射表有效性"""
    required_chars = set(
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits
    )
    return (
        len(mapping) == 62 and
        set(mapping.keys()) == required_chars and
        len(set(mapping.values())) == 62
    )

def save_reverse_mapping(mapping, filename):
    try:
        reverse_mapping = {}
        # 修改日志提示方式（移除self引用）
        conflict_log = []
        for k, v in mapping.items():
            if v in reverse_mapping:
                conflict_log.append(f"冲突警告：{v} 已被 {reverse_mapping[v]} 映射")
            reverse_mapping[v] = k
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reverse_mapping, f, ensure_ascii=False, indent=2)
            
        return conflict_log  # 返回冲突日志供调用者处理
    except Exception as e:
        raise RuntimeError(f"保存映射表失败：{str(e)}")
    
# ... [保留原有固定映射表和替换函数代码] ...
# 新增随机字符串生成函数（放在Application类外）
def generate_random_mapped(length=8):
    """生成指定长度的随机字母数字组合"""
    # chars = string.ascii_letters + string.digits
    chars = string.ascii_letters  # 仅包含大小写字母
    return ''.join(random.choice(chars) for _ in range(length))


class Application(tk.Tk):
    def __init__(self):
        super().__init__()  # 必须首先初始化父类

        # 可以在文件顶部添加版本常量
        self.title(f"时代换电代码转换器 - v{VERSION}")  # 动态版本号

        # 样式配置
        self.style = ttk.Style()

        if platform.system() == 'Windows':
            self.style.theme_use('vista')  # Windows系统使用vista主题
        else:
            self.style.theme_use('clam')   # 其他系统使用clam主题

        
        # 深色系配色方案（提高可读性）
        self.style.configure("Primary.TButton", 
                            foreground="green",
                            background="#2c3e50",  # 深蓝灰
                            font=('微软雅黑', 10, 'bold'))
        
        self.style.configure("Warning.TButton", 
                            foreground="red",
                            background="#c0392b",  # 深红色
                            font=('微软雅黑', 10, 'bold'))
        
        self.style.configure("Success.TButton",
                            foreground="green",
                            background="#27ae60",  # 深绿色
                            font=('微软雅黑', 10, 'bold'))
        
        self.style.configure("Info.TButton",
                            foreground="red",
                            background="#2980b9",  # 深蓝色
                            font=('微软雅黑', 10, 'bold'))
        
        # 通用按钮样式（用于非主要操作）
        self.style.configure("TButton",
                            foreground="#2c3e50",
                            background="#ecf0f1",
                            font=('微软雅黑', 9))
        
        # 先初始化配置路径
        self.keyword_config_path = os.path.join(get_script_dir(), 'keyword_config.csv')
        
        # 先尝试加载现有配置
        self.keywords = self._load_existing_config()
        
        # 空配置保护（仅在首次运行时创建默认）
        if not self.keywords and not os.path.exists(self.keyword_config_path):
            self._create_default_keyword_config()
        else:
            # 当配置文件存在但加载失败时保留原文件
            pass

        # 初始化其他组件
        sorted_keywords = sorted(self.keywords.keys(), key=len, reverse=True)
        self.keyword_pattern = re.compile(
            r'(?<!\w)(' + '|'.join(map(re.escape, sorted_keywords)) + r')(?!\w)',
            flags=re.UNICODE
        )

        # 其余初始化代码保持不变...
        self.encoding_var = tk.StringVar(value='gb2312')
        self.encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'latin1']
        
        # 初始化应用状态
        self.selected_dir = ""
        # self.mapping, _ = generate_fixed_mapping()
        self.filter_extensions = ['.c', '.h', '.cpp', '.hpp', '.make', '.ini']
        self.log_counter = 0

        # 配置文件与脚本同目录
        MAPPING_CONFIG_PATH = os.path.join(get_script_dir(), 'mapping_config.json')
        # 修改初始化映射表的方式
        self.mapping, self.reverse_mapping = load_or_create_mapping()
        
        # 配置界面
        self._setup_main_frame()
        self.create_widgets()
        self.setup_logging()

    def extract_and_save_keywords(self):
        """提取关键字并保存到CSV文件，同时提取引号内的字符串"""
        if not self._validate_directory():
            return

        self.log_message("开始提取关键字和引号内容...")
        try:
            # 提取关键字
            keywords = self.extract_keywords_from_folder(self.selected_dir)
            keyword_csv_path = os.path.join(get_script_dir(), 'keywords_extracted.csv')
            self.save_keywords_to_csv(keywords, keyword_csv_path)
            
            # 更新关键词映射表
            self.keywords.update({kw: "" for kw in keywords})
            self._refresh_keyword_list()
            self.log_message(f"成功提取 {len(keywords)} 个关键字")

            # 提取引号内容
            quoted_strings = set()
            for root, _, files in os.walk(self.selected_dir):
                for file in files:
                    # 检查文件扩展名是否符合过滤条件
                    if any(file.endswith(ext) for ext in self.filter_extensions):
                        file_path = os.path.join(root, file)
                        self.log_message(f"正在处理文件：{file_path}")
                        quoted_strings.update(self.extract_quoted_strings_from_file(file_path))
                    else:
                        self.log_message(f"跳过文件（不符合扩展名条件）：{file}")

            # 保存引号内容
            quoted_strings_file = os.path.join(get_script_dir(), 'quoted_strings_extracted.csv')
            self.save_quoted_strings_to_file(quoted_strings, quoted_strings_file)

            self.log_message(f"成功提取 {len(quoted_strings)} 个引号内的字符串")

            # 显示完成消息
            messagebox.showinfo(
                "完成",
                f"共提取 {len(keywords)} 个关键字，保存到 {keyword_csv_path}\n"
                f"共提取 {len(quoted_strings)} 个引号内容，保存到 {quoted_strings_file}"
            )

        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _load_existing_config(self):
        """安全加载现有配置文件（自动补全空映射值）"""
        if os.path.exists(self.keyword_config_path):
            try:
                with open(self.keyword_config_path, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    if reader.fieldnames != ["Original", "Mapped"]:
                        raise ValueError("CSV文件格式错误")
                    
                    keywords = {}
                    existing_values = set()
                    
                    for row in reader:
                        original = row['Original'].strip()
                        mapped = row['Mapped'].strip()
                        
                        if not original:
                            continue  # 跳过原始词为空的行
                            
                        # 自动生成映射值逻辑
                        if not mapped:
                            # 生成唯一随机值
                            while True:
                                mapped = generate_random_mapped()
                                if mapped not in existing_values:
                                    break
                            # 记录自动生成日志
                            self.log_message(f"自动生成映射：{original} → {mapped}")
                            
                        # 冲突检测（保留最后出现的映射关系）
                        if mapped in existing_values:
                            self.log_message(f"映射冲突：{mapped} 已存在，将覆盖")
                            
                        keywords[original] = mapped
                        existing_values.add(mapped)
                    
                    return keywords
                    
            except Exception as e:
                error_backup = f"{self.keyword_config_path}.error"
                shutil.copyfile(self.keyword_config_path, error_backup)
                messagebox.showerror("配置错误", f"配置已备份至：{error_backup}\n错误：{str(e)}")
                return {}
        return {}

    def _load_keyword_config(self):
        keyword_map = {}
        if os.path.exists(self.keyword_config_path):
            try:
                with open(self.keyword_config_path, 'r', newline='', encoding='utf-8') as f:
                    # 验证CSV有效性
                    header = f.readline().strip().split(',')
                    if header != ["Original", "Mapped"]:
                        raise ValueError("CSV文件头不匹配")
                    
                    f.seek(0)
                    reader = csv.DictReader(f)
                    for row in reader:
                        keyword = row['Original'].strip()
                        mapped = row['Mapped'].strip()
                        if keyword and mapped:
                            keyword_map[keyword] = mapped
            except Exception as e:
                messagebox.showwarning("配置错误", f"CSV加载失败：{str(e)}")
                # 创建备份
                shutil.copyfile(self.keyword_config_path, f"{self.keyword_config_path}.bak")
        else:
            self._create_default_keyword_config()
        return keyword_map

    def _create_default_keyword_config(self):
        """仅在文件不存在时创建默认配置"""
        if os.path.exists(self.keyword_config_path):
            return
            
        default_pairs = [
            ('hufan', 'dady'),
            ('you', 'kitty'),
            ('usr', 'baby')
        ]
        
        try:
            with open(self.keyword_config_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Original", "Mapped"])
                for k, v in default_pairs:
                    writer.writerow([k, v])
            self.keywords = dict(default_pairs)
        except Exception as e:
            messagebox.showerror("初始化错误", f"创建默认配置失败：{str(e)}")

            
    def _setup_main_frame(self):
        self.geometry("680x450")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def _build_log_section(self, parent):
        """构建日志区域组件"""
        log_frame = ttk.LabelFrame(parent, text="操作日志")
        log_frame.grid(row=3, column=0, sticky='nsew', pady=5)
        
        # 配置日志区布局权重
        parent.rowconfigure(3, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 创建日志文本框
        self.log_text = tk.Text(log_frame, height=8, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # 滚动条
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def _refresh_keyword_list(self):
        """刷新关键词列表"""
        if not hasattr(self, 'kw_listbox') or self.kw_listbox is None:
            return  # 如果未初始化，直接返回

        self.kw_listbox.delete(0, tk.END)
        for kw, mapped in sorted(self.keywords.items()):
            self.kw_listbox.insert(tk.END, f"{kw} → {mapped}")  # 显示键值对
    
    def _add_keyword(self):
        """带映射值输入的增强版本"""
        new_kw = self.new_kw_entry.get().strip()
        if not new_kw:
            return
        
        if new_kw in self.keywords:
            messagebox.showwarning("重复添加", f"查看关键词 '{new_kw}' 已存在")
            return
        
        # 弹出映射值输入对话框
        mapped_value = tk.simpledialog.askstring(
            "映射值输入",
            f"请输入'{new_kw}'的映射值（留空自动生成）:",
            parent=self.keyword_win
        )
        
        # 用户取消输入或关闭对话框
        if mapped_value is None:  
            return
        
        # 自动生成逻辑
        if not mapped_value.strip():
            # 生成唯一随机值
            existing_values = set(self.keywords.values())
            while True:
                mapped_value = generate_random_mapped()
                if mapped_value not in existing_values:
                    break
        
        self.keywords[new_kw] = mapped_value
        self._refresh_keyword_list()
        self.new_kw_entry.delete(0, tk.END)
        
        # 自动滚动到新增条目
        last_index = self.kw_listbox.size() - 1
        self.kw_listbox.see(last_index)

    # 增强删除方法
    def _del_keyword(self):
        """删除选中关键词（处理键值对显示）"""
        selections = self.kw_listbox.curselection()
        if not selections:
            return
        
        # 收集所有要删除的关键词
        to_delete = set()
        for idx in reversed(selections):
            display_text = self.kw_listbox.get(idx)
            original = display_text.split(" → ")[0]
            to_delete.add(original)
        
        # 批量删除
        for kw in to_delete:
            if kw in self.keywords:
                del self.keywords[kw]
        
        self._refresh_keyword_list()

    def _save_keywords(self):
        """保存时执行完整性检查（扩展冲突检测）"""
        # 原始词冲突检查
        if len(self.keywords) != len(set(self.keywords.keys())):
            duplicates = [k for k,v in collections.Counter(self.keywords.keys()).items() if v>1]
            messagebox.showwarning("原始词冲突", f"发现重复原始词：{duplicates}")
            return
        
        """保存时执行完整性检查"""
        # 有效性检查
        invalid_entries = [
            k for k,v in self.keywords.items() 
            if not k.strip() or not v.strip()
        ]
        if invalid_entries:
            messagebox.showwarning("无效条目", f"发现空条目：{invalid_entries}")
            return

        # 冲突检查
        value_count = {}
        for k, v in self.keywords.items():
            value_count[v] = value_count.get(v, 0) + 1
        
        conflicts = [v for v, count in value_count.items() if count > 1]
        if conflicts:
            # 改为自动处理冲突
            for c in conflicts:
                new_value = generate_random_mapped()
                for k in [k for k,v in self.keywords.items() if v == c]:
                    self.keywords[k] = new_value
            self.log_message(f"自动修复冲突：{len(conflicts)}处")

        # 保存操作
        try:
            with open(self.keyword_config_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Original", "Mapped"])
                for k, v in sorted(self.keywords.items()):
                    writer.writerow([k, v])
            messagebox.showinfo("保存成功", "配置已更新")
        except Exception as e:
            messagebox.showerror("保存失败", str(e))
            
    def show_keywords(self):
        """显示关键词管理窗口"""
        self.keyword_win = tk.Toplevel(self)
        self.keyword_win.title("关键词管理")
        self.keyword_win.geometry("600x500")

        # 创建带滚动条的文本框
        text_frame = ttk.Frame(self.keyword_win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 添加配置来源信息
        config_status = f"配置文件路径：{self.keyword_config_path}\n"
        config_status += "✅ 配置文件存在\n" if os.path.exists(self.keyword_config_path) else "⚠️ 配置文件不存在\n"
        text.insert(tk.END, config_status + "\n")

        """增强的配置展示界面"""
         # 添加有效性检查
        total_keywords = len(self.keywords)
        unique_values = len(set(self.keywords.values())) if total_keywords > 0 else 0

        # 唯一映射率计算保护
        unique_ratio = unique_values / total_keywords if total_keywords > 0 else 0
        
        # 最长关键词检查
        longest_key = max(self.keywords.keys(), key=len) if total_keywords > 0 else "无"

        # 在计算前添加保护
        total = len(self.keywords)
        unique_ratio = len(set(self.keywords.values())) / total if total > 0 else 0
        longest = max(self.keywords.keys(), key=len) if total > 0 else "无"

        text.insert(tk.END, "\n映射有效性检查：\n")
        text.insert(tk.END, f"• 唯一映射率：{unique_ratio:.1%}\n")  # 自动处理零值
        text.insert(tk.END, f"• 最长关键词：{longest_key}\n")  # 添加空值保护
        
        # 控制面板
        control_frame = ttk.Frame(self.keyword_win)
        control_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Label(control_frame, text="新关键词:").pack(side=tk.LEFT)
        self.new_kw_entry = ttk.Entry(control_frame, width=25)
        self.new_kw_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="添加", command=self._add_keyword).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="删除选中", command=self._del_keyword).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="保存", command=self._save_keywords).pack(side=tk.RIGHT, padx=2)

        # 关键词列表
        list_frame = ttk.Frame(self.keyword_win)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.kw_listbox = tk.Listbox(
            list_frame, 
            selectmode=tk.EXTENDED,
            font=('Consolas', 10)
        )
        scrollbar = ttk.Scrollbar(list_frame, command=self.kw_listbox.yview)
        self.kw_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.kw_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 加载初始数据
        self._refresh_keyword_list()

        # 加载并显示当前关键词
        try:
            current_keywords = self._load_keyword_config()
            text.insert(tk.END, f"当前关键词总数：{len(current_keywords)}\n\n")
            for i, (k, v) in enumerate(sorted(self.keywords.items()), 1):
                text.insert(tk.END, f"{i:03d}. {k} → {v}\n")  # 显示映射关系
        except Exception as e:
            text.insert(tk.END, f"加载关键词失败：{str(e)}")
        
        text.configure(state=tk.DISABLED)

    def _validate_directory(self):
        """验证目标文件夹有效性"""
        if not self.selected_dir:
            messagebox.showerror("错误", "请先选择目标文件夹")
            return False
        if not os.path.isdir(self.selected_dir):
            messagebox.showerror("错误", f"无效的文件夹路径：{self.selected_dir}")
            return False
        return True

    # 在Application类中添加新方法
    def start_keyword_conversion(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """启动关键词转换线程"""
        self.filter_extensions = [ext.strip() for ext in self.ext_entry.get().split(',')]
        threading.Thread(target=self.run_keyword_conversion).start()

    def run_keyword_conversion(self):
        """执行独立的关键词替换"""
        if not self._validate_directory():
            return
        
        try:
            self.progress['value'] = 0
            target_files = list(self.get_target_files())
            total_files = len(target_files)
            
            for i, file_path in enumerate(target_files, 1):
                try:
                    # 添加编码自动检测
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                        detected_encoding = chardet.detect(raw_data)['encoding'] or self.encoding_var.get()
                    
                    # 使用检测到的编码重新打开文件
                    with open(file_path, 'r+', encoding=detected_encoding, errors='replace') as f:
                        content = f.read()
                        replaced = self._replace_keyword_only(content)
                        
                        # 只有内容变化时才写入
                        if content != replaced:
                            f.seek(0)
                            f.write(replaced)
                            f.truncate()
                            self.log_message(f"成功修改：{os.path.basename(file_path)}")
                        else:
                            self.log_message(f"无变化跳过：{os.path.basename(file_path)}")
                            
                except Exception as e:
                    self.log_message(f"处理失败：{file_path} - {str(e)}")
                
                self.progress['value'] = (i / total_files) * 100
                self.update_idletasks()
            
            self.show_result(True, "关键词替换完成！")
        except Exception as e:
            self.log_message(f"系统错误：{str(e)}")

    def start_char_mapping(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """启动字符映射线程"""
        self.filter_extensions = [ext.strip() for ext in self.ext_entry.get().split(',')]
        threading.Thread(target=self.run_char_mapping).start()

    def run_char_mapping(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """执行独立的字符映射"""
        self._execute_conversion(is_char_mapping=True)

    def _execute_conversion(self, is_char_mapping):
        """通用转换执行方法"""
        try:
            self.progress['value'] = 0
            target_files = list(self.get_target_files())
            total_files = len(target_files)
            
            for i, file_path in enumerate(target_files, 1):
                try:
                    with open(file_path, 'r+', encoding=self.encoding_var.get(), errors='replace') as f:
                        content = f.read()
                        
                        # 根据标志位执行不同替换
                        if is_char_mapping:
                            replaced = self._replace_char_only(content)
                        else:
                            replaced = self._replace_keyword_only(content)
                        
                        f.seek(0)
                        f.write(replaced)
                        f.truncate()
                    self.log_message(f"成功处理：{os.path.basename(file_path)}")
                except Exception as e:
                    self.log_message(f"处理失败：{file_path} - {str(e)}")
                
                self.progress['value'] = (i / total_files) * 100
                self.update_idletasks()
            
            self.show_result(True, f"{'字符映射' if is_char_mapping else '关键词替换'}完成！")
        except Exception as e:
            self.log_message(f"系统错误：{str(e)}")

    def _replace_keyword_only(self, content):
        """仅执行关键词替换（带调试日志）"""
        def replacer(match):
            original = match.group(1)
            mapped = self.keywords.get(original, original)
            if original != mapped:
                self.log_message(f"替换关键词: {original} → {mapped}")
            return mapped
        
        return self.keyword_pattern.sub(replacer, content)

    def _replace_char_only(self, content):
        """仅执行字符映射"""
        trans_table = str.maketrans(self.mapping)
        return content.translate(trans_table)

    def check_mapping_conflicts(self):
        """检查映射冲突（用于恢复前验证）"""
        value_map = {}
        conflicts = []
        
        with open(self.keyword_config_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                original = row['Original'].strip()
                mapped = row['Mapped'].strip()
                
                if mapped in value_map:
                    conflicts.append(f"{mapped} → {value_map[mapped]} 与 {original}")
                value_map[mapped] = original
        
        if conflicts:
            msg = "发现反向映射冲突：\n" + "\n".join(conflicts)
            return messagebox.askyesno(
                "映射冲突", 
                msg + "\n\n是否继续恢复？可能会覆盖部分映射关系"
            )
        return True
    # 添加恢复方法
    def start_keyword_restore(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """关键词恢复"""
        if not os.path.exists(self.keyword_config_path):
            messagebox.showerror("错误", "找不到关键词映射表文件")
            return
        
        if not self.check_mapping_conflicts():
            return  # 用户取消操作
        
        threading.Thread(target=self.run_keyword_restore).start()

    def run_keyword_restore(self):
        """执行关键词恢复"""
        self._execute_restore(restore_type='keyword')

    def start_char_restore(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """字符映射恢复"""
        reverse_path = os.path.join(get_script_dir(), 'reverse_mapping.json')
        if not os.path.exists(reverse_path):
            messagebox.showerror("错误", "找不到字符反向映射表文件")
            return
        threading.Thread(target=self.run_char_restore).start()

    def run_char_restore(self):
        """执行字符映射恢复"""
        self._execute_restore(restore_type='char')

    def _execute_restore(self, restore_type):
        """通用恢复执行方法"""
        try:
            reverse_mapping = {}
            if restore_type == 'keyword':
                # 读取CSV构建反向映射表（处理多对一情况）
                with open(self.keyword_config_path, 'r') as f:
                    reader = csv.DictReader(f)
                    temp_map = {}
                    conflict_count = 0
                    
                    for row in reader:
                        mapped = row['Mapped'].strip()
                        original = row['Original'].strip()
                        if mapped in temp_map and temp_map[mapped] != original:
                            self.log_message(f"映射冲突：{mapped} 对应多个原始值")
                            conflict_count += 1
                        temp_map[mapped] = original
                    
                    if conflict_count > 0:
                        messagebox.showwarning("映射冲突", 
                            f"发现{conflict_count}处映射冲突，将使用最后出现的映射关系")
                    
                    # 按长度降序排序避免部分匹配
                    sorted_keys = sorted(temp_map.keys(), key=len, reverse=True)
                    reverse_mapping = {
                        k: temp_map[k] 
                        for k in sorted_keys
                        if k and temp_map[k]
                    }
                    
                    # 构建正则表达式模式
                    restore_pattern = re.compile(
                        r'(?<!\w)(' + '|'.join(map(re.escape, sorted_keys)) + r')(?!\w)',
                        flags=re.UNICODE
                    )
            # ... [保持原有字符恢复逻辑不变] ...

            # 修改后的恢复处理流程
            self.progress['value'] = 0
            target_files = list(self.get_target_files())
            total_files = len(target_files)
            
            for i, file_path in enumerate(target_files, 1):
                try:
                    with open(file_path, 'r+', encoding=self.encoding_var.get(), errors='replace') as f:
                        content = f.read()
                        
                        if restore_type == 'keyword':
                            # 使用正则表达式进行整词替换
                            def replacer(match):
                                return reverse_mapping[match.group(1)]
                            
                            restored = restore_pattern.sub(replacer, content)
                        else:
                            # 保持原有字符级恢复逻辑
                            restored = ''.join([reverse_mapping.get(c, c) for c in content])
                        
                        # 只有内容变化时才写入
                        if content != restored:
                            f.seek(0)
                            f.write(restored)
                            f.truncate()
                            self.log_message(f"成功恢复：{os.path.basename(file_path)}")
                        else:
                            self.log_message(f"无变化跳过：{os.path.basename(file_path)}")
                            
                except Exception as e:
                    self.log_message(f"恢复失败：{file_path} - {str(e)}")
                
                self.progress['value'] = (i / total_files) * 100
                self.update_idletasks()
            
            self.show_result(True, f"{'关键词' if restore_type == 'keyword' else '字符'}恢复完成！")
        except Exception as e:
            self.log_message(f"恢复操作异常：{str(e)}")

    # 新增：构建其他UI组件的方法
    def _build_action_buttons(self, parent):
        action_frame = ttk.LabelFrame(parent, text="功能操作区")
        action_frame.grid(row=1, column=0, pady=10, sticky='ew', padx=5)
        
        # 第一列：关键词替换操作
        kw_frame = ttk.Frame(action_frame)
        kw_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(kw_frame, text="关键词替换").pack(anchor=tk.W)
        ttk.Button(
            kw_frame,
            text="开始关键词转换",
            command=self.start_keyword_conversion,
            style="Primary.TButton"
        ).pack(fill=tk.X, pady=2, padx=5, ipady=3)  # 增加内边距
        
        ttk.Button(
            kw_frame,
            text="恢复关键词转换",
            command=self.start_keyword_restore,
            style="Warning.TButton"
        ).pack(fill=tk.X, pady=2, padx=5, ipady=3)  # 增加内边距

        # 第二列：字符映射操作
        char_frame = ttk.Frame(action_frame)
        char_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(char_frame, text="字符映射").pack(anchor=tk.W)
        ttk.Button(
            char_frame,
            text="开始字符映射",
            command=self.start_char_mapping,
            style="Success.TButton"
        ).pack(fill=tk.X, pady=2, padx=5, ipady=3)  # 增加内边距
        
        ttk.Button(
            char_frame,
            text="恢复字符映射",
            command=self.start_char_restore,
            style="Info.TButton"
        ).pack(fill=tk.X, pady=2, padx=5, ipady=3)  # 增加内边距

        # 公共操作按钮
        common_frame = ttk.Frame(action_frame)
        common_frame.pack(side=tk.LEFT, padx=10)
        ttk.Button(common_frame, text="映射表", command=self.show_mapping).grid(row=0, column=0, padx=2)
        ttk.Button(common_frame, text="关键词", command=self.show_keywords).grid(row=0, column=1, padx=2)


    def _build_progress_bar(self, parent):
        self.progress = ttk.Progressbar(parent, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.grid(row=2, column=0, sticky='ew', pady=5)

    def refresh_mapping(self):
        MAPPING_CONFIG_PATH = os.path.join(get_script_dir(), 'mapping_config.json')
        if os.path.exists(MAPPING_CONFIG_PATH):
            os.remove(MAPPING_CONFIG_PATH)
        self.mapping, self.reverse_mapping = load_or_create_mapping()
        messagebox.showinfo("完成", "已生成新映射表")

    def create_widgets(self):
        # 主容器
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # 配置区组件
        self._build_config_section(main_frame)
        
        # 新增：操作按钮区
        self._build_action_buttons(main_frame)
        
        # 新增：进度条
        self._build_progress_bar(main_frame)
        
        # 新增：日志区
        self._build_log_section(main_frame)

        # 修复按钮添加方式
        ttk.Button(
            self.config_frame,  # 使用实例变量
            text="刷新映射表", 
            command=self.refresh_mapping
        ).grid(row=0, column=4, padx=5, sticky='e')  # 添加具体布局参数

        ttk.Button(
            self.config_frame,
            text="提取关键字",
            command=self.extract_and_save_keywords
        ).grid(row=0, column=5, padx=10, sticky='e')
    
    def _build_config_section(self, parent):
        self.config_frame = ttk.LabelFrame(parent, text="配置设置")
        self.config_frame.grid(row=0, column=0, sticky='ew', pady=5)
        
        # 文件扩展名设置
        ttk.Label(self.config_frame, text="文件扩展名:").grid(row=0, column=0, sticky='w', padx=5)
        self.ext_entry = ttk.Entry(self.config_frame, width=25)
        self.ext_entry.grid(row=0, column=1, sticky='ew', padx=5)
        self.ext_entry.insert(0, ".c, .h, .cpp, .hpp, .make, .ini")

        # 编码选择设置（修复组合框定义）
        ttk.Label(self.config_frame, text="文件编码:").grid(row=0, column=2, sticky='w', padx=5)
        # 正确代码
        self.encoding_combo = ttk.Combobox(
            self.config_frame,
            textvariable=self.encoding_var,
            values=self.encodings,
            width=12,
            state='readonly'
        )
        self.encoding_combo.grid(row=0, column=3, sticky='ew', padx=5)

        # 刷新按钮（添加具体布局参数）
        ttk.Button(
            self.config_frame,
            text="刷新映射表",
            command=self.refresh_mapping
        ).grid(row=0, column=4, padx=5, sticky='e')

        # 配置列权重
        self.config_frame.columnconfigure(1, weight=1)
        self.config_frame.columnconfigure(3, weight=1)
        self.config_frame.columnconfigure(4, weight=1)

        # 目录选择部分
        dir_frame = ttk.Frame(self.config_frame)
        dir_frame.grid(row=1, column=0, columnspan=5, pady=5, sticky='ew')  # 修正跨列数
        
        ttk.Label(dir_frame, text="目标文件夹:").pack(side=tk.LEFT)
        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(dir_frame, text="浏览...", command=self.select_directory).pack(side=tk.RIGHT)


    def _filter_keywords(self, content):
        """过滤C/C++关键词并返回受保护的位置集合"""
        keyword_positions = set()
        # 查找所有关键词并记录字符位置
        for match in self.keyword_pattern.finditer(content):
            start, end = match.span()
            keyword_positions.update(range(start, end))
        return keyword_positions
    
    # 保留其他方法不变...
    def select_directory(self):
        dir_path = filedialog.askdirectory(title="选择目标文件夹")
        if dir_path:
            self.selected_dir = dir_path
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dir_path)
            self.log_message(f"已选择目录：{dir_path}")
        else:  # 用户取消选择时清空路径
            self.selected_dir = ""
            self.dir_entry.delete(0, tk.END)

    def show_result(self, success, message):
        if success:
            messagebox.showinfo("操作成功", message)
        else:
            messagebox.showerror("操作失败", message)  
    
    def setup_logging(self):
        if not os.path.exists('operation.log'):
            open('operation.log', 'w').close()
            
    def log_message(self, message, show_gui=True):
        """增强的日志记录方法"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[AutoFix] {timestamp} - {message}\n"
        
        # 写入文件日志
        with open('operation.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        # 更新GUI日志
        if show_gui and hasattr(self, 'log_text'):
            self.log_text.configure(state=tk.NORMAL)
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            self.log_text.configure(state=tk.DISABLED)
    
    def show_mapping(self):
        mapping_window = tk.Toplevel(self)
        mapping_window.title("字符映射表预览")
        
        tree = ttk.Treeview(mapping_window, columns=('Original', 'Mapped'), show='headings')
        tree.heading('Original', text="原始字符")
        tree.heading('Mapped', text="映射字符")
    
        # 显示所有字符映射关系
        for k, v in self.mapping.items():
            tree.insert('', tk.END, values=(k, v))  # 不再过滤小写字母
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def start_conversion(self):
        self.filter_extensions = [ext.strip() for ext in self.ext_entry.get().split(',')]
        threading.Thread(target=self.run_conversion).start()

    # 没啥用了,可以删除
    def run_restore(self):
        """执行恢复操作的完整实现"""
        try:
            # 改为：
            reverse_path = os.path.join(get_script_dir(), 'reverse_mapping.json')
            with open(reverse_path, 'r', encoding='utf-8') as f:
                reverse_mapping = json.load(f)

            self.progress['value'] = 0
            total_files = sum(1 for _ in self.get_target_files())
            processed = 0

            for root, _, files in os.walk(self.selected_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in self.filter_extensions):
                        path = os.path.join(root, file)
                        try:
                            with open(path, 'r+', encoding=self.encoding_var.get(), errors='replace') as f:
                                content = f.read()
                                restored = ''.join([reverse_mapping.get(c, c) for c in content])
                                f.seek(0)
                                f.write(restored)
                                f.truncate()
                            self.log_message(f"成功恢复文件：{path}")
                        except Exception as e:
                            self.log_message(f"恢复失败：{path} - {str(e)}")
                        
                        processed += 1
                        self.progress['value'] = (processed / total_files) * 100
                        self.update_idletasks()

            self.show_result(True, f"恢复完成！共处理{processed}个文件")
        except Exception as e:
            self.log_message(f"恢复操作异常：{str(e)}")
            self.show_result(False, f"恢复失败：{str(e)}")
            
    # 没啥用了,可以删除
    def start_restore(self):
        if not os.path.exists('reverse_mapping.json'):
            messagebox.showerror("错误", "找不到反向映射表文件")
            return
        threading.Thread(target=self.run_restore).start()

    def _replace_keywords(self, content):
        """执行两阶段替换：关键词→字符映射"""
        # 阶段1：关键词替换
        def keyword_replacer(match):
            original = match.group(0)
            mapped = self.keywords.get(original, original)
            if mapped != original:
                self.log_message(f"关键词替换: {original} → {mapped}")
            return mapped
        
        # 按长度降序排序避免部分匹配
        sorted_keys = sorted(self.keywords.keys(), key=len, reverse=True)
        keyword_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b'
        )
        phase1_content = keyword_pattern.sub(keyword_replacer, content)
        
        # 阶段2：字符级映射
        phase2_content = []
        for c in phase1_content:
            # 保留已替换关键词的内容
            phase2_content.append(self.mapping.get(c, c))
        return ''.join(phase2_content)

    def run_conversion(self):
        """执行转换操作的完整实现"""
        self.progress['value'] = 0
        total_files = sum(1 for _ in self.get_target_files())
        
        processed = 0
        for root, _, files in os.walk(self.selected_dir):
            for file in files:
                if any(file.endswith(ext) for ext in self.filter_extensions):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r+', encoding=self.encoding_var.get(), errors='replace') as f:
                            content = f.read()
                            # 调用修正后的替换方法
                            replaced = self._replace_keywords(content)
                            
                            f.seek(0)
                            f.write(replaced)
                            f.truncate()
                        self.log_message(f"成功处理文件：{path}")
                    except Exception as e:  # 添加缺失的except块
                        self.log_message(f"处理失败：{path} - {str(e)}")
                    
                    processed += 1
                    self.progress['value'] = (processed / total_files) * 100
                    self.update_idletasks()
        
        self.show_result(True, f"转换完成！共处理{processed}个文件")
        reverse_path = os.path.join(get_script_dir(), 'reverse_mapping.json')
        save_reverse_mapping(self.mapping, reverse_path)
    
    def get_target_files(self):
        for root, _, files in os.walk(self.selected_dir):
            for file in files:
                if any(file.endswith(ext) for ext in self.filter_extensions):
                    yield os.path.join(root, file)
    
    # ... [保留原有目录选择和其他方法] ...

    @staticmethod
    def extract_keywords_from_file(file_path,file_names):
        """从单个文件中提取关键字，并过滤长度小于等于 MIN_KEYWORD_LENGTH 的词"""
        # 正则表达式：匹配函数名和变量名，排除引号内的内容和 /* ... */ 注释块
        keyword_pattern = re.compile(
            r'(?<!["\'])\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?=\s*[\(;:])(?!["\'])'
        )
        block_comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)  # 匹配 /* ... */
        quoted_string_pattern = re.compile(r'"([^"]*)"')  # 匹配 "xxx" 中的内容
        class_name_pattern = re.compile(r'\b\w+::')  # 匹配类名::模式

        keywords = set()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # 移除 /* ... */ 注释块
                content = block_comment_pattern.sub('', content)

                # 移除双引号内的内容
                content = quoted_string_pattern.sub('', content)

                # 移除类名::模式
                content = class_name_pattern.sub('', content)

                # 提取关键字
                matches = keyword_pattern.findall(content)
                keywords.update(
                    match for match in matches 
                    if len(match) > MIN_KEYWORD_LENGTH and match not in C_KEYWORDS and match not in EXCLUDED_IDENTIFIERS and (file_names is None or match not in file_names)
                )
        except Exception as e:
            print(f"无法读取文件 {file_path}：{str(e)}")
        return keywords

    @staticmethod
    def extract_keywords_from_folder(folder_path):
        """从文件夹中提取所有.c和.h文件的关键字"""
        all_keywords = set()
        extensions = ['.c', '.h', '.cpp', '.hpp', '.make', '.cpp']
        file_names = set()  # 用于存储文件名

        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    # 提取文件名（不带扩展名）
                    file_name = os.path.splitext(file)[0]
                    file_names.add(file_name)

        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    # 通过类名调用静态方法
                    keywords = Application.extract_keywords_from_file(file_path,file_names)
                    all_keywords.update(keywords)

        return all_keywords

    @staticmethod
    def save_keywords_to_csv(keywords, output_file):
        """将关键字保存到CSV文件，仅保存长度大于 MIN_KEYWORD_LENGTH 的关键字"""
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Keyword"])
                # 使用全局常量过滤长度大于 MIN_KEYWORD_LENGTH 的关键字
                for keyword in sorted(keyword for keyword in keywords if len(keyword) > MIN_KEYWORD_LENGTH):
                    writer.writerow([keyword])
        except Exception as e:
            raise RuntimeError(f"保存失败：{str(e)}")

    @staticmethod
    def extract_quoted_strings_from_file(file_path):
        """从单个文件中提取引号内的字符串"""
        # 正则表达式匹配双引号内的内容
        quoted_pattern = re.compile(r'"([^"]*)"')  # 匹配"xxx"中的内容
        quoted_strings = set()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = quoted_pattern.findall(content)
                # 添加所有匹配的引号内容到集合中
                quoted_strings.update(matches)
        except Exception as e:
            print(f"无法读取文件 {file_path}：{str(e)}")
        return quoted_strings


    @staticmethod
    def save_quoted_strings_to_file(quoted_strings, output_file):
        """将引号内的字符串保存到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for string in sorted(quoted_strings):
                    f.write(f'"{string}"\n')  # 每行保存一个引号内容，保留引号
        except Exception as e:
            raise RuntimeError(f"保存失败：{str(e)}")


    def extract_and_save_quoted_strings(self):
        """提取引号内的字符串并保存到文件"""
        if not self._validate_directory():
            return

        self.log_message("开始提取引号内的字符串...")
        try:
            # 调用静态方法提取所有引号内的字符串
            quoted_strings = set()
            for root, _, files in os.walk(self.selected_dir):
                for file in files:
                    # 检查文件扩展名是否符合过滤条件
                    if any(file.endswith(ext) for ext in self.filter_extensions):
                        file_path = os.path.join(root, file)
                        self.log_message(f"正在处理文件：{file_path}")
                        quoted_strings.update(self.extract_quoted_strings_from_file(file_path))
                    else:
                        self.log_message(f"跳过文件（不符合扩展名条件）：{file}")

            # 保存提取结果到文件
            quoted_strings_file = os.path.join(get_script_dir(), 'quoted_strings_extracted.txt')
            self.save_quoted_strings_to_file(quoted_strings, quoted_strings_file)

            self.log_message(f"成功提取 {len(quoted_strings)} 个引号内的字符串")
            messagebox.showinfo(
                "完成",
                f"共提取 {len(quoted_strings)} 个引号内的字符串，已保存到 {quoted_strings_file}"
            )
        except Exception as e:
            messagebox.showerror("错误", str(e))

if __name__ == "__main__":
    app = Application()
    app.mainloop()