# qlog path_id validation POC

This repository is a small proof of concept for semantic checks around the event-level `path_id` field discussed in [issue #20](https://github.com/huitema/qlog-multipath-extension/issues/20).

## Run

Requires Python 3 and uses only the standard library:

```sh
python3 scripts/check_path_id_validation.py
```

The examples cover the unsigned 32-bit boundaries, `common_fields` inheritance and consistency, known-path versus connection-wide events, missing identifiers, and incorrect placement inside `data`.

## Scope

This is an exploratory semantic checker for a small set of example traces. It does not compile CDDL or validate traces against the complete qlog main, QUIC, and multipath schemas. The multipath draft and its CDDL profile remain in the [qlog-multipath-extension repository](https://github.com/huitema/qlog-multipath-extension). The checker can help discuss validation rules and examples; it is not a conformance validator.
