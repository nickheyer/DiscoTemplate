export const FIELD_SORT = {
  'discord-bot-configuration': [
      'prefix_keyword',
      'discord_token'
  ],
  'debug-configuration': [
      'is_verbose_logging',
      'is_debug'
  ],
  'misc-configuration': [
      'session_timeout',
      'max_check_time',
      'max_results',
      'max_seasons_for_non_admin',
      'is_trailers_enabled'
  ]
};

export const ADDITIONAL_USER_SETTINGS = {
  'session_timeout': {
      VERBOSE: 'Session Timeout',
      TYPE: 'INT',
      DEFAULT: 60
  },
  'is_superuser': {
      VERBOSE: 'Server Owner / Super User',
      TYPE: 'BOOL',
      DEFAULT: false
  },
  'is_staff': {
      VERBOSE: 'Grant Database Access',
      TYPE: 'BOOL',
      DEFAULT: false
  },
  'password': {
      VERBOSE: 'Database Access Password',
      TYPE: 'PASSWORD',
      DEFAULT: ''
  }
};
