import perf
import json
from yosai_libauthz import is_permitted_from_json, is_permitted_from_str

rust_lib = "/home/dowwie/MyProjects/yosai_libauthz/target/release/libauthz.so"

assigned_perms = [x.encode('utf-8') for x in
                  ["domain1:action3:target1", "domain1:action1,action2", "domain1:action4:target2"]]

serialized_perms = json.dumps([{'domain': 'domain1', 'actions': ['action3'], 'targets': ['target1']},
                               {'domain': 'domain1', 'actions': ['action1','action2']},
                               {'domain': 'domain1', 'actions': ['action4'], 'targets': ['target2']}])

required_perm = "domain1:action4:target3".encode('utf-8')
lib = ctypes.cdll.LoadLibrary(rust_lib)


def bench_is_permitted_from_json():
    is_permitted_from_json(required_perm, serialized_perms)


def bench_is_permitted_from_str():
    is_permitted_from_str(required_perm, assigned_perms)


if __name__ == "__main__":
    runner = perf.Runner()
    print("JSON Benchmark:")
    runner.timeit("test_permission", "bench_is_permitted_from_json()",
                  "from __main__ import bench_is_permitted_from_json", inner_loops=10)

    print("\n\nString Benchmark:")
    runner.timeit("test_permission", "bench_is_permitted_from_str()",
                  "from __main__ import bench_is_permitted_from_str", inner_loops=10)
