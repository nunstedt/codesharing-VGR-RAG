# Module Dependency Graph

```
main.py
├── config.py
├── data_init.py
└── mode_logic.py
    ├── profile_manager.py
    │   └── system_user_profile.py (existing)
    └── chat_session.py
        └── query_handler.py
            ├── chat_memory.py (existing)
            ├── query_metadata_extractor.py (existing)
            ├── prompt_assistant.py (existing)
            ├── prompt_QA.py (existing)
            └── index.py (existing)

External Dependencies (unchanged):
├── LLM.py
├── ingest.py
├── langdetect
└── llama_index.*
```

## Call Flow

### Profile Mode:
```
main.py → mode_logic.run_profile_mode() → profile_manager.create_new_profile()
```

### Compliance Mode:
```
main.py → mode_logic.run_compliance_mode()
├── profile_manager.select_system()
└── chat_session.ComplianceChatSession
    └── query_handler.* (various functions)
```

### QA Mode:
```
main.py → mode_logic.run_qa_mode()
└── chat_session.QAChatSession
    └── query_handler.* (various functions)
```

## Key Abstractions

1. **ChatSession**: Base class for all interactive modes
2. **ComplianceChatSession**: Adds system context to prompts
3. **QAChatSession**: Uses general Q&A prompts
4. **query_handler**: Shared utilities for all chat modes
5. **profile_manager**: System profile CRUD operations
6. **config**: Centralized configuration
7. **data_init**: One-time setup operations
