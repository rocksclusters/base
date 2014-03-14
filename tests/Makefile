# Run tests
#
# Copyright (c) 2005 Junio C Hamano
#

-include ../config.mak.autogen
-include ../config.mak

#ROCKS_TEST_OPTS = --verbose --debug
SHELL_PATH ?= /bin/sh
TAR ?= /bin/tar
RM ?= rm -f
PROVE ?= prove
DEFAULT_TEST_TARGET ?= test
TEST_LINT ?= test-lint-duplicates test-lint-executable

ifdef TEST_OUTPUT_DIRECTORY
TEST_RESULTS_DIRECTORY = $(TEST_OUTPUT_DIRECTORY)/test-results
else
TEST_RESULTS_DIRECTORY = test-results
endif

# Shell quote;
SHELL_PATH_SQ = $(subst ','\'',$(SHELL_PATH))
TEST_RESULTS_DIRECTORY_SQ = $(subst ','\'',$(TEST_RESULTS_DIRECTORY))

T = $(sort $(wildcard t[0-9][0-9][0-9][0-9]-*.sh))

all: $(DEFAULT_TEST_TARGET)

test: pre-clean $(TEST_LINT)
	$(MAKE) aggregate-results-and-cleanup

prove: pre-clean $(TEST_LINT)
	@echo "*** prove ***"; $(PROVE) --exec '$(SHELL_PATH_SQ)' $(ROCKS_PROVE_OPTS) $(T) :: $(ROCKS_TEST_OPTS)
	$(MAKE) clean-except-prove-cache

$(T):
	@echo "*** $@ ***"; '$(SHELL_PATH_SQ)' $@ $(ROCKS_TEST_OPTS)

pre-clean:
	$(RM) -r '$(TEST_RESULTS_DIRECTORY_SQ)'

clean-except-prove-cache:
	$(RM) -r 'trash_directory'.* '$(TEST_RESULTS_DIRECTORY_SQ)'

clean: clean-except-prove-cache
	$(RM) .prove

test-lint: test-lint-duplicates test-lint-executable

test-lint-duplicates:
	@dups=`echo $(T) | tr ' ' '\n' | sed 's/-.*//' | sort | uniq -d` && \
		test -z "$$dups" || { \
		echo >&2 "duplicate test numbers:" $$dups; exit 1; }

test-lint-executable:
	@bad=`for i in $(T); do test -x "$$i" || echo $$i; done` && \
		test -z "$$bad" || { \
		echo >&2 "non-executable tests:" $$bad; exit 1; }

aggregate-results-and-cleanup: $(T)
	$(MAKE) aggregate-results
	$(MAKE) clean

aggregate-results:
	for f in '$(TEST_RESULTS_DIRECTORY_SQ)'/t*-*.counts; do \
		echo "$$f"; \
	done | '$(SHELL_PATH_SQ)' ./aggregate-results.sh

.PHONY: pre-clean $(T) aggregate-results clean valgrind perf
