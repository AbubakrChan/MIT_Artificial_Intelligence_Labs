from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain

# Example 1

rule1 = IF ('parent (?y) (?x)', THEN('self (?x) (?x)'))

rule2 = IF( AND( 'parent (?x) (?y)',
                 'parent (?x) (?z)',
                 NOT('self (?y) (?z)') ),
            THEN( 'sibling (?y) (?z)') )

data = ['parent marge bart', 'parent marge lisa']

print('Example 1')
print(forward_chain([rule1, rule2], data, verbose=True))

# Example 2
rule1 = IF( AND( '(?x) has chocolate',
                 '(?x) likes eating chocolate'),
            THEN( '(?x) is happy') )

data = ['Bill has chocolate', 'Alex has chocolate', 'Alex likes eating chocolate']

print('\nExample 2')
print(forward_chain([rule1], data, verbose=True))

# Exmaple 3
rule1 = IF( AND( '(?x) is a bird',
                 NOT ('(?x) is a penguin')),
            THEN( '(?x) is a chicken') )

# rule2 = IF( AND( NOT ('(?x) is a penguin'),
#                  '(?x) is a bird'),
#             THEN ('(?x) is a chicken'))
# A NOT expresion should never introduce new variables, because it would have infinite bindings for (?x)

data = ['Phil is a penguin', 'Sue is a bird']

print('\nExample 3')
print(forward_chain([rule1], data, verbose=True))

# Example 4:
theft_rule = IF( 'you have (?x)',
                 THEN( 'i have (?x)' ),
                 DELETE( 'you have (?x)' ))

data = ('you have apple', 'you have orange', 'you have pear')

print('\nExample 4')
print(forward_chain([theft_rule], data, verbose=True))














